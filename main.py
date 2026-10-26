from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs
from app.config.database import init_db
from app.controllers.itinerario_controller import submit
from app.views.page import page

class Handler(BaseHTTPRequestHandler):
    def output(self, text, status=200):
        encoded=text.encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type','text/html; charset=utf-8')
        self.send_header('Content-Length',str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)
    def do_GET(self):
        if self.path!='/': return self.output('<h1>No encontrado</h1>',404)
        self.output(page())
    def do_POST(self):
        if self.path!='/generar': return self.output('<h1>No encontrado</h1>',404)
        length=int(self.headers.get('Content-Length','0'))
        if length>10000: return self.output(page(error='Formulario demasiado grande.'),413)
        data=parse_qs(self.rfile.read(length).decode('utf-8'),keep_blank_values=True)
        try:
            result=submit({k:v if k=='intereses' else v[0] for k,v in data.items()})
            self.output(page(result=result))
        except (ValueError,OverflowError) as e:
            self.output(page(error=str(e)),400)

if __name__=='__main__':
    init_db()
    server=ThreadingHTTPServer(('127.0.0.1',8000),Handler)
    print('Ayacucho Conecta: http://127.0.0.1:8000')
    try: server.serve_forever()
    except KeyboardInterrupt: server.server_close()

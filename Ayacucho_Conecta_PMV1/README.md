# Ayacucho Conecta — PMV1

Demostración académica de generación básica de itinerarios para Ayacucho. Datos y precios ilustrativos; no apta para tomar decisiones reales de viaje.

## Ejecutar (Python 3.10+)
```bash
python main.py
```
Abrir **http://127.0.0.1:8000**. Salir con Ctrl+C.

## Probar
```bash
python -m unittest discover -s tests -v
```

## Estructura y decisiones
- MVC: `app/views`, `app/controllers`, `app/models`
- SQLite en `app/config/database.py`; tablas `atractivos`, `itinerarios`, `itinerario_detalle`
- Diagramas PlantUML: `docs/`
- Versionado: Git/GitHub. Publicar en una cuenta del equipo; no hay URL simulada.

## Límites
Sin autenticación, agencias, reservas, pagos, PWA instalable, datos oficiales, geolocalización ni optimización de rutas. El algoritmo es una selección sencilla por filtros y capacidad de 8 h por día, no IA. Antes de uso real validar horarios, rutas, tiempos y costos. No subas datos personales ni claves al repositorio.

## Evidencia sugerida
Capturas de la página inicial, generación exitosa, validación de error, terminal de tests y enlace real del repositorio. Registrar fecha y responsables en el Word.

import os
import sqlite3
from pathlib import Path

DEFAULT_PATH = Path(__file__).resolve().parents[2] / 'ayacucho.sqlite3'
PLACES = [
 ('Plaza Mayor de Ayacucho','cultura',0,1),
 ('Complejo arqueológico de Wari','cultura',15,3),
 ('Pampa de Ayacucho','cultura',10,3),
 ('Aguas Turquesas de Millpu','naturaleza',50,6),
 ('Mirador de Acuchimay','naturaleza',0,2),
 ('Ruta gastronómica local','gastronomia',40,2),
 ('Caminata paisajística','aventura',25,4),
]
# Importes y tiempos únicamente ficticios para demostración; no son tarifas oficiales.
def connect(db_path=None):
    path=str(db_path or os.environ.get('AYACUCHO_DB',DEFAULT_PATH))
    db=sqlite3.connect(path)
    db.row_factory=sqlite3.Row
    db.execute('PRAGMA foreign_keys=ON')
    return db

def init_db(db_path=None):
    with connect(db_path) as db:
        db.executescript("""
            CREATE TABLE IF NOT EXISTS atractivos(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL, interes TEXT NOT NULL,
                costo REAL NOT NULL CHECK(costo>=0),
                duracion INTEGER NOT NULL CHECK(duracion>0));
            CREATE TABLE IF NOT EXISTS itinerarios(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                dias INTEGER NOT NULL, presupuesto REAL NOT NULL,
                intereses TEXT NOT NULL, costo_estimado REAL NOT NULL,
                creado_en TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP);
            CREATE TABLE IF NOT EXISTS itinerario_detalle(
                itinerario_id INTEGER NOT NULL REFERENCES itinerarios(id),
                atractivo_id INTEGER NOT NULL REFERENCES atractivos(id),
                dia INTEGER NOT NULL, PRIMARY KEY(itinerario_id, atractivo_id));
        """)
        if db.execute('SELECT COUNT(*) FROM atractivos').fetchone()[0]==0:
            db.executemany('INSERT INTO atractivos(nombre,interes,costo,duracion) VALUES(?,?,?,?)',PLACES)

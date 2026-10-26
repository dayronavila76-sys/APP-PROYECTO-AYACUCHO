import sqlite3
import tempfile
import unittest
from pathlib import Path
from app.config.database import init_db
from app.controllers.itinerario_controller import submit

class Tests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.db=str(Path(self.temp.name)/'test.db')
        init_db(self.db)
    def tearDown(self): self.temp.cleanup()
    def test_cp01_valid_save(self):
        data=submit({'dias':'3','presupuesto':'300','intereses':['cultura']},self.db)
        self.assertGreater(data['id'],0)
        with sqlite3.connect(self.db) as db:
            self.assertEqual(db.execute('SELECT COUNT(*) FROM itinerarios').fetchone()[0],1)
            self.assertGreater(db.execute('SELECT COUNT(*) FROM itinerario_detalle').fetchone()[0],0)
    def test_cp02_invalid_days(self):
        with self.assertRaises(ValueError): submit({'dias':'0','presupuesto':'100','intereses':['cultura']},self.db)
    def test_cp03_invalid_budget(self):
        with self.assertRaises(ValueError): submit({'dias':'2','presupuesto':'0','intereses':['cultura']},self.db)
    def test_cp04_missing_interest(self):
        with self.assertRaises(ValueError): submit({'dias':'2','presupuesto':'100','intereses':[]},self.db)
    def test_cp05_invalid_not_saved(self):
        with self.assertRaises(ValueError): submit({'dias':'2','presupuesto':'abc','intereses':['cultura']},self.db)
        with sqlite3.connect(self.db) as db:
            self.assertEqual(db.execute('SELECT COUNT(*) FROM itinerarios').fetchone()[0],0)
    def test_cp06_no_budget_options(self):
        with self.assertRaises(ValueError): submit({'dias':'1','presupuesto':'1','intereses':['gastronomia']},self.db)

if __name__=='__main__': unittest.main()

import sys, os
import psycopg2
from dotenv import load_dotenv

# Force utf-8 partout
os.environ['PYTHONIOENCODING'] = 'utf-8'
if hasattr(sys, 'setfilesystemencoding'):
    sys.setfilesystemencoding('utf-8')

load_dotenv()
print("DB:", os.environ.get("POSTGRES_DB"))
print("USER:", os.environ.get("POSTGRES_USER"))
print("PWD:", os.environ.get("POSTGRES_PASSWORD"))
print("HOST:", os.environ.get("POSTGRES_HOST"))
print("PORT:", os.environ.get("POSTGRES_PORT"))
import psycopg2
try:
    conn = psycopg2.connect(
        dbname="wulin",
        user="wulinuser",
        password="TestWushu2025",
        host="localhost",
        port="5432",
    )
    print("Connexion directe OK")
except Exception as e:
    print("Erreur directe:", repr(e))


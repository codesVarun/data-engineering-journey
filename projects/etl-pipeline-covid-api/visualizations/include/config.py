import os
from dotenv import load_dotenv
import psycopg2

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
DOTENV_PATH = os.path.join(ROOT_DIR, '.env')

if not os.environ.get("POSTGRES_HOST"):
    load_dotenv(dotenv_path=DOTENV_PATH)

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT",),
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD")
    )
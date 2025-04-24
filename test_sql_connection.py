from sqlalchemy import create_engine
import urllib
import os
from dotenv import load_dotenv

load_dotenv()

SQL_SERVER = os.getenv('SQL_SERVER')
SQL_DATABASE = os.getenv('SQL_DATABASE')
SQL_USERNAME = os.getenv('SQL_USERNAME')
SQL_PASSWORD = os.getenv('SQL_PASSWORD')

params = urllib.parse.quote_plus(
    f'DRIVER={{ODBC Driver 18 for SQL Server}};'
    f'SERVER={SQL_SERVER},1433;'
    f'DATABASE={SQL_DATABASE};'
    f'UID={SQL_USERNAME};'
    f'PWD={SQL_PASSWORD};'
    f'Encrypt=yes;TrustServerCertificate=no;'
)

print("String de conexão gerada:", params)  # Para depuração

engine = create_engine(f'mssql+pyodbc:///?odbc_connect={params}')

try:
    with engine.connect() as conn:
        result = conn.execute("SELECT GETDATE()")
        for row in result:
            print(f"✅ Conectado! Data atual: {row[0]}")
except Exception as e:
    print(f"Erro: {e}")
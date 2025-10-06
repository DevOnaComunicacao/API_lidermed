import mysql.connector
from pathlib import Path
from mysql.connector import Error
import dotenv
import os

env_path = Path(__file__).parent / ".env"
dotenv.load_dotenv(dotenv_path=env_path)

print(os.getenv('BD_USER'))
print(os.getenv('BD_PASS'))

def get_mysql_connection():
    try:
        conn = mysql.connector.connect(
            host=os.getenv("BD_HOST"),
            user=os.getenv("BD_USER"),
            password=os.getenv("BD_PASS"),
            database=os.getenv("BD_DATABASE"),
            port=3306
        )
        if conn.is_connected():
            print("✅ Conectado ao MySQL!")
            return conn

    except Error as e:
        # Mostra a mensagem exata do MySQL
        print(f"❌ Erro ao conectar ao MySQL: {e}")

    # se chegou aqui, a conexão falhou
    return None
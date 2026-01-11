import psycopg
from dotenv import load_dotenv
from pathlib import Path
import os

def addROLES()-> None:
    data = [
    "User",
    "Admin",
    "Master"
]
    load_dotenv(Path.home() / ".config" / "myDbConfig"/ ".env")
    conn = psycopg.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )
    conn.autocommit = True
    for item in data:
        conn.execute(
            "INSERT INTO roles (role_name) VALUES (%s)",
            (item,)
        )
    conn.close()

if __name__ == "__main__":
    addROLES()
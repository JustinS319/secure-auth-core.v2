import psycopg
from dotenv import load_dotenv
from pathlib import Path
import os
load_dotenv(Path.home() / ".config" / "myDbConfig" / ".env")
def connect(sql: str, params = None):
    with psycopg.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    ) as conn:
        conn.autocommit = True
        with conn.cursor() as cur:
            cur.execute(sql, params or ())
            if cur.description:
                columns = [desc.name for desc in cur.description]
                rows = cur.fetchall()
                return columns, rows
            else:
                return f"Query executed successfully. Rows affected: {cur.rowcount}"

if __name__ == "__main__":
    result = connect("SELECT * FROM users;")
    
    if isinstance(result, tuple):
        columns, rows = result
        print("Columns:", columns)
        print("Data:")
        for row in rows:
            print(row)
    else:
        print(result)
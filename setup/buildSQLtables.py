import psycopg
from dotenv import load_dotenv
from pathlib import Path
import os
def innit()-> None:
    load_dotenv(Path.home() / ".config" / "myDbConfig"/ ".env")

    with psycopg.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    ) as conn:
    
        create_roles_table="""
CREATE TABLE IF NOT EXISTS roles(
role_id SERIAL PRIMARY KEY,
role_name VARCHAR(50) UNIQUE NOT NULL
        );
        """
        create_users_table="""
CREATE TABLE IF NOT EXISTS users(
user_id SERIAL PRIMARY KEY,
username VARCHAR(50) UNIQUE NOT NULL,
password_hash TEXT NOT NULL,
email VARCHAR(100),
lockout BOOL DEFAULT FALSE,
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        create_user_roles="""
CREATE TABLE IF NOT EXISTS user_roles(
user_id INTEGER REFERENCES users(user_id),
role_id INTEGER REFERENCES roles(role_id),
PRIMARY KEY (user_id, role_id)
        );
        """
        create_two_factor_table = """
CREATE TABLE IF NOT EXISTS two_factor (
user_id INTEGER REFERENCES users(user_id),
secret TEXT,
enabled BOOLEAN DEFAULT FALSE NOT NULL,
PRIMARY KEY (user_id)
        );
        """
        conn.autocommit = True
        for item in [create_roles_table, create_users_table, create_user_roles, create_two_factor_table]:
            conn.execute(item)
if __name__ == "__main__":
    try:
        innit()
        print("Success!!")
    except Exception as e:
        print(f"Failed: {e}")
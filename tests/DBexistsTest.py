import psycopg
from dotenv import load_dotenv
import os
def main(): 
    load_dotenv(os.path.expanduser("~/.config/mySqlApp/.env"))
    try:    
        conn = psycopg.connect(
                dbname=os.getenv("DB_NAME"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASS"),
                host=os.getenv("DB_HOST"),
                port=os.getenv("DB_PORT")
            )
        assert not conn.closed
        conn.close()
        return True, "Test Passed"
    except Exception as e:
        #print(f"Connection failed: {e}")
        return False, e
    
if __name__ == "__main__":
    testPass, status = main()
    print(status)
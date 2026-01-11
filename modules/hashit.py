from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from setup import connectDB
from argon2 import PasswordHasher

ph = PasswordHasher(memory_cost=262144)
def hashPassword(password):
    hash = ph.hash(password)
    return hash
def get_existingHash(user):
    sql = "SELECT password_hash FROM users WHERE username = %s;"
    _, rows = connectDB.connect(sql, (user,))
    hash_value = rows[0][0] if rows else None
    return hash_value
def verify(hash_value, user):
    hash = get_existingHash(user)
    try:
        ph.verify(hash, hash_value)
        return "Password match"
    except Exception as e:
        return f"error: {e}"
if __name__=="__main__":
    print(hashPassword("Pass"))

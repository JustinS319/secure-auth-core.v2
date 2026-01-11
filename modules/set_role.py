from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from setup.connectDB import connect


def role(username):
    columns, rows = connect("SELECT 1 FROM user_roles LIMIT 1;")
    is_first_user = (len(rows) == 0)
    role_id = 3 if is_first_user else 1
    columns, rows = connect(
        "SELECT user_id FROM users WHERE username = %s;",
        (username,)
    )
    if len(rows) == 0:
        raise ValueError("User not found")
    user_id = rows[0][0]
    columns, rows = connect(
        "SELECT role_id FROM user_roles WHERE user_id = %s;",
        (user_id,)
    )
    if len(rows) > 0:
        return rows[0][0]
    connect(
        "INSERT INTO user_roles (user_id, role_id) VALUES (%s, %s);",
        (user_id, role_id)
    )
    return role_id

if __name__ == "__main__":
    role("Justin")
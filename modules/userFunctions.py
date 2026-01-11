from getpass import getpass
import otp
import random
import string
from typing import Optional
import re
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from setup.connectDB import connect
import modules.hashit as hashit
import set_role
import loginMain
def getUserdata()-> tuple[str, str, str]:
    usernameAttempt= 0
    while usernameAttempt < 3:
        base_name = input("Please enter your name:\n")
        if not base_name:
            print("Can not be blank. Please try again")
            usernameAttempt +=1
            continue
        for _ in range(10):
            suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=3))
            candidate = f"{base_name}_{suffix}"

            if userExist(candidate) is None:
                username = candidate
                print(f"Your username is {username}. Please write it down.")
                print("You will be able to change it later.")
                break                              
            else:
                print("Couldn't find an available username with that name. Try a different name.")
                usernameAttempt += 1
                continue
        break
    if usernameAttempt == 3:
        print("Too many attempts.")
        return None, None, None
    password =  Password()
    if password == None:
        return None, None, None
    emailAttempts = 0
    while emailAttempts < 3:
        email = input("Please provide your email address for password resets:\n")
        regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        match = re.fullmatch(regex, email)
        if match:
            break
        else:
            print("Invalid email. Please try again.")
            emailAttempts += 1
    if emailAttempts == 3:
        return None, None, None
    
    return username, password, email
def userExist(usr):
    _, rows = connect("SELECT user_id FROM users WHERE username = %s;", (usr,))
    try:
        user_id = rows[0][0] if rows else None
        return int(user_id)
    except:
        return None
def CreateUser(username: Optional[str] = None, password: Optional[str] = None, email: Optional[str] = None, create = False):
    sql = "INSERT INTO users (username, password_hash, email) VALUES(%s, %s, %s);" 
    if not all [username, email, password]:
        data = getUserdata()
        username,password, email = data
    if not create:
        return loginMain.login(username, password, email)
    if username == None:
        return "Error: Malformed data"
    connect(sql, (username, password, email))
    set_role.role(username)
    set2fa(username)
    return "User account created successfully"
def set2fa(username):
    sql = "INSERT INTO two_factor (user_id, enabled) VALUES (%s, %s);"
    enabled = input("Would you like to enable two factor authentication?(yes/no)\n").lower()
    _, rows = connect("SELECT user_id FROM users WHERE username = %s;",(username,))
    user_id = rows[0][0]
    
    if enabled in ["y", "yes"]:
        otp.generate_qrCLI(username)
        print("2fa Enabled.")
        return
    elif enabled in ["n","no"]:
        print("2fa will not be enabled. This can be changed later.")
    else:
        print("Sorry didn't recognize that command. Setting two factor to false you may change this later.")
    enabled = False
    connect(sql, (user_id, enabled,))
def Password():
    passwordAttempts = 0
    while passwordAttempts < 3:
        pass1 = getpass("Please enter a password:\t")
        pass2 = getpass("Please confirm password:\t")
        if pass1 == pass2:
            pass1 = hashit.hashPassword(pass1)
            return pass1
        passwordAttempts += 1
    print("Too many failed attempts.")
    return None
if __name__ == "__main__":
    CreateUser()

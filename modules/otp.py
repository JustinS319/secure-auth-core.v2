from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from setup.connectDB import connect
import pyotp
import qrcode
from userFunctions import userExist
def generate_qrCLI(user)-> bool:
    code = generate_totp(user, True)#Always pass true
    uri_code = code.provisioning_uri(name=user,issuer_name= "SecureAuthCore v2.0")
    qr = qrcode.QRCode()
    qr.add_data(uri_code)
    qr.make(fit=True)
    qr.print_ascii()
    return verify_totp(code)
def generate_secret(user_id):
    secret = pyotp.random_base32()
    connect("""
INSERT INTO two_factor (user_id, secret, enabled) 
VALUES (%s, %s, TRUE)
ON CONFLICT (user_id) DO UPDATE SET secret = EXCLUDED.secret, enabled = TRUE;""",(user_id, secret, ) )
    return secret
def generate_totp(user, enable = False):
    if enable == False:
        return
    user_id = userExist(user)
    _, rows = connect("Select secret, enabled From two_factor WHERE user_id = %s",(user_id,))
    if not rows:
        generate_secret(user_id)
        _, rows = connect("Select secret, enabled From two_factor WHERE user_id = %s",(user_id,))
    enabled = rows[0][1]
    if not enabled:
        if enable == False:
            return False
    key = rows[0][0]
    key = str(key).strip()
    if key == None:
        key = generate_secret(user_id)
    totp = pyotp.TOTP(key)
    return totp
def verify_totp(totp, input_code = None):
    if not input_code:
        input_code = input("Please enter 2fa code: ")
    if not totp.verify(input_code):
        return False
    return True
def login_2fa(username, code = None):
    user_id = userExist(username)
    _, rows = connect("SELECT secret, enabled FROM two_factor WHERE user_id = %s", (user_id,))
    if rows and rows[0][1]:   
        secret = rows[0][0]
        if not secret:
            return False
        totp = pyotp.TOTP(secret)
        if not verify_totp(totp, code):
            return False
    else:
        return True
if __name__ == "__main__":
    generate_secret(1)

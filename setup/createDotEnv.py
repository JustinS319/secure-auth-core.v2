from pathlib import Path
import sys
def get_input(prompt: str, default: str) -> str:
    value = input(f"{prompt} [defaults to {default}]:    ").strip()
    return value if value else default
def dbDATA()-> tuple [str, str, str, str, str]:
    dbname = input("Please enter the database name:    ")
    dbuser = input("Please enter the database user name:    ")
    dbpass = input("Please enter the database user password:    ")
    dbhost = get_input("Please enter the database host:", "localhost")
    dbport = get_input("Please enter the database host port:", "5432")
    return dbname, dbuser, dbpass, dbhost, dbport
def create_config()-> None:
    config_dir = Path.home() / ".config" / "myDbConfig"
    config_dir.mkdir(parents=True, exist_ok=True)
    env_path = config_dir / ".env"
    if env_path.exists():
        print(f"Config already exists at {env_path}")
        contin = input("Would you like to continue with the rest of setup anyways?").lower()
        if contin  not in ("yes", "y"):
            print("Please delete the config file to regenerate it via the setup program.")
            sys.exit()
    else:
        dbname, dbuser, dbpass, dbhost, dbport = dbDATA()
        default_content = f"""
DB_NAME={dbname}
DB_USER={dbuser}
DB_PASS={dbpass}
DB_HOST={dbhost}
DB_PORT={dbport}
        """
        env_path.write_text(default_content)
        print(f"Created config at {env_path}")
if __name__ == "__main__":
    create_config()
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from createDotEnv import create_config
from buildSQLtables import innit
from addRoles import addROLES
from pathlib import Path
FILE_PATH = Path.home() / ".config" / "myDbConfig" / "setupComplete.flag"
def run_setup(f = FILE_PATH)-> tuple[bool, str]:
    f.parent.mkdir(parents=True, exist_ok=True)
    if not f.exists():
        try:
            create_config()
            print("Starting table creation....")
            innit()
            print("Adding roles....")
            addROLES()
        except Exception as e:
            return False, e
        f.write_text("initialized")
        return True, "Setup Complete!"
    else:
        return True, "Setup completed previously."
if __name__ == "__main__":
    _, e = run_setup()
    print(e)
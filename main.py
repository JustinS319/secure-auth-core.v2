from setup.setupMain import run_setup  

def startUP(): 
        _ , result = run_setup()
        if _ == True:
                if result != "Setup completed previously.":
                        print("Setup completed.")
        else:
                return f"Error during setup: {result}"
def MainCLI():
        print("Welcome to the interactive CLI mode of the Auth core system.")
        print("This an interactive user authentication system that utilizes PostgreSQL.")
        print("If this is your first time running the program setup will be run creating everything needed for the system to run.")
        
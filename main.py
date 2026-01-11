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
        print("")
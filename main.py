from setup.setupMain import run_setup  
import sys
import time
def startUP(): 
        _ , result = run_setup()
        if _ == True:
                if result != "Setup completed previously.":
                        return True, "Setup completed."
                else:
                        return True, None
        else:
                return False, f"Error during setup: {result}"
def MainCLI():
        print("Welcome to the interactive CLI mode of the Auth core system.")
        time.sleep(1)
        print("This an interactive user authentication system that utilizes PostgreSQL.")
        time.sleep(1)
        print("If this is your first time running the program, setup will be run creating everything needed for the system to run.")
        time.sleep(1)
        print("Initiating setup......")
        passFail, comm = startUP()
        if comm:
                print(comm)
        if not passFail:
                print("Program will shutdown. Please restart and try again")
                print("Exiting ", end="", flush=True)
                for _ in range(6):
                        print(". ", end="", flush=True)
                        time.sleep(0.5)
                sys.exit()

if __name__ == "__main__":
        MainCLI()
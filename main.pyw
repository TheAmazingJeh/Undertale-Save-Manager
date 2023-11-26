import sys, os

# Gets the current directory that the program is running in
def get_current_dir():
    # If the program is frozen, get the directory of the executable
    if getattr(sys, 'frozen', False):
        loc = os.path.dirname(sys.executable)
        # Change the working directory to the executable directory
        os.chdir(loc)
    else:
        # Get the directory of the script
        loc = os.path.dirname(os.path.realpath(__file__))
    return loc

# Add the lib folder to the path, so that the program can find the modules
sys.path.insert(0, "lib")
# Import the main window and run it
from lib.libUndertaleSaveManager import UndertaleSaveManager


if __name__ == "__main__":
    # Create the main window
    w = UndertaleSaveManager(get_current_dir())
    # Run the main loop
    w.mainloop()
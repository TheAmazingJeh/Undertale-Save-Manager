import os, sys, json, base64
from tkinter import Tk, Frame, Button, Listbox, Scrollbar, StringVar, END, ACTIVE, E, W, N, S, PhotoImage
from tkinter.messagebox import  askyesnocancel, showinfo, showerror
from tkinter.simpledialog import askstring

from lib.popup.GameTypeSelect import GameTypeSelect
from lib.popup.SettingsMenu import Settings
from lib.filemanip.SaveFileOperations import backup_save, write_save
from lib.PyinstallerExeUtils import close_splash, get_icon
from lib.windowmanip.SetWindowMiddle import set_window_middle
from lib.filemanip.FileValidation import is_save

class UndertaleSaveManager(Tk):
    def __init__(self, loc:str):
        # Initialize the window
        super().__init__()
        
        # Hide the window until it's ready to be shown
        self.withdraw()

        # Get the current directory
        self.loc = loc
        # Load the config file, and save it to a temporary variable so it can be accessed later
        self.temp_config = self.load_config()

        # Set the program data
        self.program_data = {
            # Location of the Undertale data folder that contains the active save
            "data":os.path.join(os.getenv("LOCALAPPDATA"), "UNDERTALE"),
            # Location of the folder that contains the backup saves
            "savesFolder": os.path.join(self.loc, "Saves"),
            # Constant location of the folder that contains the backup saves
            "savesFolderCONST": os.path.join(self.loc, "Saves"),
            # Location of the Undertale executable
            "exe":self.temp_config["exe"],
        }
        # If the game type is in the config file, set it to the temporary gane type variable
        if "GAMETYPE" in self.temp_config:
            self.program_data["GAMETYPE"] = self.temp_config["GAMETYPE"]
        
        # Delete the temporary config variable
        del self.temp_config

        self.save_config()

        self.pre_start()
        self.create_window()
        self.refresh_saves()

        # Show the window
        self.deiconify()

    # Creates the window
    def create_window(self):
        # Set the window title and icon
        self.title("Save Manager")
        icon = get_icon()
        if icon[0] == "base64":
            self.wm_iconphoto(True, PhotoImage(data=icon[1]))
        elif icon[0] == "path":
            self.iconbitmap(icon[1])
        
        # Set the window size and make it unresizable
        set_window_middle(self, 464,220)
        self.resizable(False, False)

        # Set the right frame, which contains the buttons to backup and load saves as well as other buttons
        self.right_frame = Frame(self)

        Button(self.right_frame, text="Backup Loaded Save", command=self.backup_save_gui).grid(row=0, column=1, sticky=E)
        Button(self.right_frame, text="Load Selected Save", command=self.write_save_gui).grid(row=1, column=1, sticky=E)
        
        Button(self.right_frame, text="Settings", command=self.open_settings).grid(row=3, column=1, sticky=E)
        #Button(self.right_frame, text="Download Save Files", command=self.download_saves).grid(row=4, column=1, sticky=E)
        Button(self.right_frame, text="Quit", command=sys.exit).grid(row=5, column=1, sticky=E+N)
        
        self.right_frame.grid(row=0, column=0, padx=2, pady=2)

        # Set the saves frame, which contains the list of saves
        self.saves_frame = Frame(self)

        self.saves_list = Listbox(self.saves_frame, height=10, width=50)
        self.saves_list.grid(row=0, column=0, columnspan=3, sticky=W)
        self.scrollbar = Scrollbar(self.saves_frame)
        self.scrollbar.grid(row=0, column=3, sticky=N+S)
        self.saves_list.config(yscrollcommand = self.scrollbar.set)
        self.scrollbar.config(command = self.saves_list.yview)

        self.saves_frame.grid(row=0, column=1, padx=10, pady=10, sticky=E)

        # Set the left frame, which contains the button to open the game
        self.left_frame = Frame(self)

        self.launchGameText = StringVar()
        self.launchGameText.set(self.update_game_button())
        Button(self.left_frame, textvariable=self.launchGameText, command=self.open_game).grid(row=0, column=0, sticky=W)

        self.left_frame.grid(row=1, column=1, padx=10, sticky=W)


        # Set the bottom frame, which contains the buttons to refresh the saves list, open the folder, and go back a folder
        self.bottom_frame = Frame(self)

        Button(self.bottom_frame, text="Refresh", command=self.refresh_saves).grid(row=0, column=0, sticky=E)
        Button(self.bottom_frame, text="Open Folder", command=self.open_folder).grid(row=0, column=1, sticky=W)
        Button(self.bottom_frame, text="Back", command=self.back_folder).grid(row=0, column=2, sticky=E)

        self.bottom_frame.grid(row=1, column=1, padx=10, sticky=E)

    # Loads the config file
    def load_config(self):
        # If the config file doesn't exist, create it
        if not os.path.exists(os.path.join(self.loc, "config.json")):
            with open(os.path.join(self.loc, "config.json"), 'w') as f:
                defaultConfig = {
                    "exe":None,
                }
                # Write the default config to the config file
                json.dump({}, f, indent=4)

        # Load the config file
        with open(os.path.join(self.loc, "config.json"), 'r') as f:
            # Set the config file to a variable
            vars = json.load(f)
            saveFlag = False
            # If the exe isn't in the config file, set it to None and save the config file
            if "exe" not in vars:
                vars["exe"] = None
                saveFlag = True
            # If the config has changed, save the config file
            if saveFlag:
                with open(os.path.join(self.loc, "config.json"), 'w') as f:
                    json.dump(vars, f, indent=4)
        # Return the config file
        return vars

    # Saves the config file
    def save_config(self):
        # Save the config file
        with open(os.path.join(self.loc, "config.json"), 'w') as f:
            json.dump(self.program_data, f, indent=4)

    # Assorted Functions that need to be run before the window is created
    def pre_start(self):
        # Checks if the data folder exists
        if not os.path.exists(self.program_data["data"]):
            # If it doesn't, show an error and exit
            close_splash()
            showerror("Error","No save file found.\nPlease make sure you have installed Undertale & have ran it at least once.")
            sys.exit()
        # Checks if the saves folder exists
        if not os.path.exists(self.program_data["savesFolder"]):
            # If it doesn't, create it
            os.makedirs(self.program_data["savesFolder"])
        
        # Close the splash screen
        close_splash()

    # Saves List - Opens selected Folder
    def open_folder(self):
        # Check if the selected save is a folder or a save
        if is_save(os.path.join(self.program_data["savesFolder"], self.get_selected_option())):
            # If it's a save, show an error and return
            showerror("Error","Selected option is a folder, not a save.")
            return
        # Set the saves folder to the selected folder
        self.program_data["savesFolder"] = os.path.join(self.program_data["savesFolder"], self.get_selected_option())
        # Refresh the saves list, with the new saves folder
        self.refresh_saves()

    # Saves List - Goes back a folder
    def back_folder(self):
        # Check if the current saves folder is the constant saves folder, if it is, return
        if self.program_data["savesFolder"] == self.program_data["savesFolderCONST"]: return
        # Set the saves folder to the parent folder of the current saves folder
        self.program_data["savesFolder"] = os.path.dirname(self.program_data["savesFolder"])
        # Refresh the saves list, with the new saves folder
        self.refresh_saves()

    # Gets the selected option from the list
    def get_selected_option(self):
        # Get the selected option
        value=str((self.saves_list.get(ACTIVE)))
        # Remove the save and folder tags
        value = value.replace("  [Save]","")
        value = value.replace("  [Folder]","")
        value = value.strip()
        # Return the selected option
        return value

    # Clears the saves list and refreshes it
    def refresh_saves(self):
        # Clear the saves list
        self.saves_list.delete(0,END)
        # Get the saves in the current saves folder
        items_for_saves = self.get_saves(self.program_data["savesFolder"])
        # Add the saves to the saves list
        for items in items_for_saves:
            self.saves_list.insert(END,items)

    # Presents a GUI for backing up the current save
    def backup_save_gui(self):
        # Ask the user for a name for the new save
        new_save = askstring("Backup","Please enter a name for the new save. Seperate folders with \\\\")
        # If the user doesn't cancel, backup the save
        if new_save == None:
            return
        # If the user doesn't enter a name, show an error
        elif new_save == "":
            showerror("Error","Please enter a name for the new save.")
            return
        # If the user enters a name, backup the save
        else:
            backup_save(new_save, self.program_data, self.loc)
            showinfo("Success",f"Your Save, '{new_save}' has been backed up.")

        self.refresh_saves()

    # Presents a GUI for writing a backup to the current save
    def write_save_gui(self):
        # Check if the selected save is a folder or a save, if it's a folder, show an error and return
        if not is_save(os.path.join(self.program_data["savesFolder"], self.get_selected_option())):
            showerror("Error","You can't load a folder.")
            return

        # Get the current save directory
        data = self.program_data["data"]
        # Check if the current save exists, if it does, ask the user if they want to overwrite it
        if os.path.exists(os.path.join(data, "undertale.ini")):
            oversave = askyesnocancel("Warning","A save already exists. Do you want to overwrite it?")
            # If the user says no, ask them for a name for the old save, so it can be backed up
            if oversave == False:
                new_save = askstring("Backup","Please enter a name for the old save, so it can be backed up.")
                # If the user doesn't cancel, backup the save
                if new_save != None:
                    backup_save(new_save, self.program_data, self.loc)
                # If the user cancels, return
                else:
                    return
            # If the user cancels, return
            if oversave != True and oversave != False:
                return
            
            # Write the save to the current save
            write_save(self.get_selected_option(), self.program_data)
            # Show a success message
            showinfo("Success",f"Your Save, '{self.get_selected_option()}' has been loaded.")

    # Opens Settings
    def open_settings(self):
        # Show the settings window
        settings = Settings(self, self.loc, self.program_data)
        # Update the game launch button text, as the game type may have changed
        self.launchGameText.set(self.update_game_button())

    # Updates the game launch button text to display the current game launch type    
    def update_game_button(self):
        # Get the game type from the config
        match "GAMETYPE" in self.program_data:
            # If the game type is set, set the game launch button text to display the game type
            case True: gameL = f" ({self.program_data['GAMETYPE'][0]})"
            # If the game type isn't set, set the game launch button text to display nothing
            case _: gameL = ""
        # Return the game launch button text
        return "Launch Game"+gameL

    # Gets all the saves in a folder (for the saves list)
    def get_saves(self, path:str):
        # Get the saves in the folder
        saves = os.listdir(path)
        # Add the save and folder tags to the saves
        for i in range(len(saves)):
            # If the save is a folder, add the folder tag
            if not is_save(os.path.join(self.program_data['savesFolder'], saves[i])): saves[i] = "  [Folder] " + saves[i]
            # If the save is a save, add the save tag
            else: saves[i] = "  [Save] " + saves[i]

        # Return the saves
        return saves

    # Prompts the user to select a game type
    def get_game_type(self):
        # Shows the game type select window
        window = GameTypeSelect(self, self.loc)
        result = window.result
        # If the user cancels, return the current config
        if result == None:
            return self.program_data
        # If the user selects a game type, save it to the config
        self.program_data["GAMETYPE"] = result
        with open(os.path.join(self.loc, 'config.json'), 'w') as f:
            json.dump(self.program_data, f, indent=4)
        # Update the game button text
        self.launchGameText.set(self.update_game_button())
        # Return the config
        return self.program_data

    # Opens the game using the specified method
    def open_game(self):
        # If the user hasn't selected a game type, prompt them to do so
        if not "GAMETYPE" in self.program_data:
            self.program_data = self.get_game_type()
        # If the game type exists, open the game using the specified method
        else:
            os.system(self.program_data["GAMETYPE"][1])

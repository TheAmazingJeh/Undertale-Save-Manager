from tkinter import *
import os, sys, ctypes, json
from tkinter.messagebox import  askyesnocancel, showinfo, showerror
from tkinter.simpledialog import askstring

from gameTypeSelect import GameTypeSelect
from settingsMenu import Settings

# Tries to import the splash screen, but doesn't error if it doesn't exist (for pyinstaller)
try: 
    import pyi_splash
except ImportError:
    pass

# Closes the splash screen, if it exists (for pyinstaller)
def close_splash(): 
    try:
        pyi_splash.close()
    except NameError:
        pass

# ----- File Functions ----- #
def open_file(file_name): 
    try:
        with open(file_name, 'r') as file:
            return file.read()
    except FileNotFoundError:
        return ""

def save_file(file_name, data): # Saves a file
    with open(file_name, 'w') as file:
        file.write(data)

def try_to_delete(file_name): # Tries to delete a file, but doesn't error if it doesn't exist
    try:
        os.remove(file_name)
    except FileNotFoundError:
        pass

class UndertaleSaveManager(Tk):
    def __init__(self):
        super().__init__()

        self.loc = self.get_current_dir()
        self.temp_config = self.load_config()

        self.program_data = {
            "data":os.path.join(os.getenv("LOCALAPPDATA"), "UNDERTALE"),
            "savesFolder": os.path.join(self.loc, "Saves"),
            "savesFolderCONST": os.path.join(self.loc, "Saves"),
            "exe":self.temp_config["exe"],
        }
        if "GAMETYPE" in self.temp_config:
            self.program_data["GAMETYPE"] = self.temp_config["GAMETYPE"]
        
        del self.temp_config

        self.save_config()

        self.pre_start()
        self.create_window()
        self.refresh_saves()

    def get_current_dir(self):
        if getattr(sys, 'frozen', False):
            loc = os.path.dirname(sys.executable)
            os.chdir(loc)
        else:
            loc = os.path.dirname(os.path.realpath(__file__))
        return loc

    def create_window(self):
        # ----- Window Settings ------ #
        self.title("Save Manager")
        if os.path.exists(os.path.join(self.loc,"UNDERTALE.ico")):
            self.iconbitmap(os.path.join(self.loc, "UNDERTALE.ico"))
            
        self.configure()
        self.set_window_middle(464,220)
        self.resizable(False, False)

        #------ Top Left Buttons ------#
        self.right_frame = Frame(self)

        Button(self.right_frame, text="Backup Loaded Save", command=self.backup_save_gui).grid(row=0, column=1, sticky=E)
        Button(self.right_frame, text="Load Selected Save", command=self.write_save_gui).grid(row=1, column=1, sticky=E)
        
        Button(self.right_frame, text="Settings", command=self.open_settings).grid(row=3, column=1, sticky=E)
        #Button(self.right_frame, text="Download Save Files", command=self.download_saves).grid(row=4, column=1, sticky=E)
        Button(self.right_frame, text="Quit", command=sys.exit).grid(row=5, column=1, sticky=E+N)
        
        self.right_frame.grid(row=0, column=0, padx=2, pady=2)

        #--------- Saves List ---------#
        self.saves_frame = Frame(self)

        self.saves_list = Listbox(self.saves_frame, height=10, width=50)
        self.saves_list.grid(row=0, column=0, columnspan=3, sticky=W)
        self.scrollbar = Scrollbar(self.saves_frame)
        self.scrollbar.grid(row=0, column=3, sticky=N+S)
        self.saves_list.config(yscrollcommand = self.scrollbar.set)
        self.scrollbar.config(command = self.saves_list.yview)

        self.saves_frame.grid(row=0, column=1, padx=10, pady=10, sticky=E)

        #------- Bottom Left Buttons --------#
        self.left_frame = Frame(self)

        self.launchGameText = StringVar()
        self.launchGameText.set(self.update_game_button())
        Button(self.left_frame, textvariable=self.launchGameText, command=self.open_game).grid(row=0, column=0, sticky=W)

        self.left_frame.grid(row=1, column=1, padx=10, sticky=W)


        #------- Bottom Right Buttons -------#
        self.bottom_frame = Frame(self)

        Button(self.bottom_frame, text="Refresh", command=self.refresh_saves).grid(row=0, column=0, sticky=E)
        Button(self.bottom_frame, text="Open Folder", command=self.open_folder).grid(row=0, column=1, sticky=W)
        Button(self.bottom_frame, text="Back", command=self.back_folder).grid(row=0, column=2, sticky=E)

        self.bottom_frame.grid(row=1, column=1, padx=10, sticky=E)

    # Loads the config file
    def load_config(self):
        if not os.path.exists(os.path.join(self.loc, "config.json")):
            with open(os.path.join(self.loc, "config.json"), 'w') as f:
                defaultConfig = {
                    "exe":None,
                }
                
                json.dump({}, f, indent=4)
        with open(os.path.join(self.loc, "config.json"), 'r') as f:
            vars = json.load(f)
            saveFlag = False
            if "exe" not in vars:
                vars["exe"] = None
                saveFlag = True
            if saveFlag:
                with open(os.path.join(self.loc, "config.json"), 'w') as f:
                    json.dump(vars, f, indent=4)
        return vars
        
        

    # Saves the config file
    def save_config(self):
        with open(os.path.join(self.loc, "config.json"), 'w') as f:
            json.dump(self.program_data, f, indent=4)

    # Assorted Functions that need to be run before the window is created
    def pre_start(self):
        if not os.path.exists(self.program_data["data"]): # Checks if the data folder exists
            close_splash()
            showerror("Error","No save file found.\nPlease make sure you have installed Undertale & have ran it at least once.")
            sys.exit()
        if not os.path.exists(self.program_data["savesFolder"]):
            os.makedirs(self.program_data["savesFolder"])
        
        close_splash()

    # Sets the window to the middle of the screen
    def set_window_middle(self, width:int, height:int):
        user32 = ctypes.windll.user32
        screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1) # Multi Monitor Fix
        middle = screensize[0] // 2, screensize[1] // 2
        add = middle[0] - width // 2, middle[1] - height // 2
        self.geometry(f"{width}x{height}+{add[0]}+{add[1]}")

    # Checks if a directory is a save or not
    def is_save(self, path:str):
        f = []
        for (dirpath, dirnames, filenames) in os.walk(path):
            f.extend(filenames)
            break
        if len(f) > 0:
            return True
        else:
            return False

    # Saves List - Opens selected Folder
    def open_folder(self):
        if self.is_save(os.path.join(self.program_data["savesFolder"], self.get_selected_option())):
            showerror("Error","Selected option is a folder, not a save.")
            return
        self.program_data["savesFolder"] = os.path.join(self.program_data["savesFolder"], self.get_selected_option())
        self.refresh_saves()

    # Saves List - Goes back a folder
    def back_folder(self):
        if self.program_data["savesFolder"] == self.program_data["savesFolderCONST"]: return
        self.program_data["savesFolder"] = os.path.dirname(self.program_data["savesFolder"])
        self.refresh_saves()

    # Gets the selected option from the list
    def get_selected_option(self):
        value=str((self.saves_list.get(ACTIVE)))
        value = value.replace("  [Save]","")
        value = value.replace("  [Folder]","")
        value = value.strip()
        return value

    # Clears the saves list and refreshes it
    def refresh_saves(self):
        self.saves_list.delete(0,END)
        items_for_saves = self.get_saves(self.program_data["savesFolder"])
        for items in items_for_saves:
            self.saves_list.insert(END,items)

    # Backs up the current save as specified name
    def backup_save(self, new_name:str):
        if not os.path.isdir(self.loc+f"\\Saves\\{new_name}"):
            os.makedirs(self.loc+f"\\Saves\\{new_name}")

        save_file(self.loc+f"\\Saves\\{new_name}\\file0",open_file(self.program_data["data"] + "\\file0"))
        save_file(self.loc+f"\\Saves\\{new_name}\\file9",open_file(self.program_data["data"] + "\\file9"))
        save_file(self.loc+f"\\Saves\\{new_name}\\file8",open_file(self.program_data["data"] + "\\file8"))
        save_file(self.loc+f"\\Saves\\{new_name}\\undertale.ini",open_file(self.program_data["data"] + "\\undertale.ini"))
        print(f"\nSave backed up as '{new_name}'\n")

    # Presents a GUI for backing up the current save
    def backup_save_gui(self):
        new_save = askstring("Backup","Please enter a name for the new save. Seperate folders with \\\\")
        if new_save != None:
            self.backup_save(new_save)
            showinfo("Success",f"Your Save, '{new_save}' has been backed up.")

    # Writes specified backup to the current save
    def write_save(self, backup_name:str):
        try_to_delete(self.program_data["data"] + "\\file0")
        try_to_delete(self.program_data["data"] + "\\file9")
        try_to_delete(self.program_data["data"] + "\\undertale.ini")
        try_to_delete(self.program_data["data"] + "\\file8")
        
        save_file(self.program_data["data"] + "\\file0",open_file(self.program_data["savesFolder"] + f"\\{backup_name}\\file0"))
        save_file(self.program_data["data"] + "\\file9",open_file(self.program_data["savesFolder"] + f"\\{backup_name}\\file9"))
        save_file(self.program_data["data"] + "\\file8",open_file(self.program_data["savesFolder"] + f"\\{backup_name}\\file8"))
        save_file(self.program_data["data"] + "\\undertale.ini",open_file(self.program_data["savesFolder"] + f"\\{backup_name}\\undertale.ini"))

    # Presents a GUI for writing a backup to the current save
    def write_save_gui(self):
        # Check if the selected save is a folder or a save
        if not self.is_save(os.path.join(self.program_data["savesFolder"], self.get_selected_option())):
            showerror("Error","You can't load a folder.")
            return

        data = self.program_data["data"]
        if os.path.exists(f"{data}\\undertale.ini"):
            oversave = askyesnocancel("Warning","A save already exists. Do you want to overwrite it?")
            if oversave == False:
                new_save = askstring("Backup","Please enter a name for the old save, so it can be backed up.")
                if new_save != None:
                    self.backup_save(new_save)
                else:
                    return
            if oversave != True and oversave != False:
                return
            self.write_save(self.get_selected_option())
            showinfo("Success",f"Your Save, '{self.get_selected_option()}' has been loaded.")

    # Opens Settings
    def open_settings(self):
        settings = Settings(self, self.loc, self.program_data)
        settings = settings.result
        self.launchGameText.set(self.update_game_button())
        return
    
    def update_game_button(self): # Updates the game button text to display the current game launch type
        match "GAMETYPE" in self.program_data:
            case True: gameL = f" ({self.program_data['GAMETYPE'][0]})"
            case _: gameL = ""
        return "Launch Game"+gameL

    # Gets all the saves in a folder (for the saves list)
    def get_saves(self, path:str):
        saves = os.listdir(path)
        for i in range(len(saves)):
            if not self.is_save(f"{self.program_data['savesFolder']}\\{saves[i]}"): saves[i] = "  [Folder] " + saves[i]
            else: saves[i] = "  [Save] " + saves[i]
        return saves



    def get_game_type(self): # Prompts the user to select a game type
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

    def open_game(self): # Opens the game using the specified method
        # If the user hasn't selected a game type, prompt them to do so
        if not "GAMETYPE" in self.program_data:
            self.program_data = self.get_game_type()
        # If the game type exists, open the game using the specified method
        else:
            os.system(self.program_data["GAMETYPE"][1])

if __name__ == "__main__":
    w = UndertaleSaveManager()
    w.mainloop()
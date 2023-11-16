from tkinter import *
import os, sys, ctypes
from tkinter.messagebox import  askyesnocancel, showinfo, showerror, showwarning
from tkinter.simpledialog import askstring

# Tries to import the splash screen, but doesn't error if it doesn't exist (for pyinstaller)
try: 
    import pyi_splash
except ImportError:
    pass

# Changes the working directory to the location of the script (for pyinstaller)
def get_current_dir():
    if getattr(sys, 'frozen', False):
        loc = os.path.dirname(sys.executable)
        os.chdir(loc)
    else:
        loc = os.path.dirname(os.path.realpath(__file__))
    return loc

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

# ----- Tkinter Classes ----- #

class UndertaleSaveManager(Tk):
    def __init__(self):
        super().__init__()

        self.location_data = {
            "exe":"C:\\Program Files (x86)\\Steam\\steamapps\\common\\Undertale",
            "data":os.getenv("LOCALAPPDATA")+"\\UNDERTALE",
            "savesFolder": loc+"\\Saves",
            "savesFolderCONST": loc+"\\Saves"
        }

        self.pre_start()

        # ----- Window Settings ------ #
        self.title("Save Manager")
        if os.path.exists(loc+"\\UNDERTALE.ico"):
            self.iconbitmap(loc+"\\UNDERTALE.ico")
            
        self.configure()
        self.set_window_middle(464,220)
        self.resizable(False, False)

        #-------- Left Buttons --------#
        self.right_frame = Frame(self)

        Button(self.right_frame, text="Backup Loaded Save", command=self.backup_save_gui).grid(row=0, column=1, sticky=E)
        Button(self.right_frame, text="Load Selected Save", command=self.write_save_gui).grid(row=1, column=1, sticky=E)
        Button(self.right_frame, text="Refresh Saves List", command=self.refresh_saves).grid(row=2, column=1, sticky=E)
        #Button(self.right_frame, text="Download Save Files", command=self.download_saves).grid(row=4, column=1, sticky=E)
        Button(self.right_frame, text="Quit", command=sys.exit).grid(row=5, column=1, sticky=E+N)
        
        self.right_frame.grid(row=0, column=0, padx=2, pady=2)

        #--------- Saves List ---------#
        self.saves_frame = Frame(self)

        self.saves_list = Listbox(self.saves_frame, height=10, width=50)
        self.saves_list.grid(row=0, column=0)
        self.scrollbar = Scrollbar(self.saves_frame)
        self.scrollbar.grid(row=0, column=1, sticky=N+S)
        self.saves_list.config(yscrollcommand = self.scrollbar.set)
        self.scrollbar.config(command = self.saves_list.yview)

        self.saves_frame.grid(row=0, column=1, padx=10, pady=10, sticky=E)

        #------- Bottom Buttons -------#
        self.bottom_frame = Frame(self)

        Button(self.bottom_frame, text="Open Folder", command=self.open_folder).grid(row=0, column=0, sticky=W)
        Button(self.bottom_frame, text="Back", command=self.back_folder).grid(row=0, column=1, sticky=E)

        self.bottom_frame.grid(row=1, column=1, padx=10, sticky=E)

        #--------- Saves List ---------#
        self.refresh_saves()

    # Assorted Functions that need to be run before the window is created
    def pre_start(self):
        if not os.path.exists(self.location_data["data"]): # Checks if the data folder exists
            close_splash()
            showerror("Error","No save file found.\nPlease make sure you have installed Undertale & have ran it at least once.")
            sys.exit()
        if not os.path.exists(loc+"\\Saves"):
            os.makedirs(loc+"\\Saves")

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
        if self.is_save(os.path.join(self.location_data["savesFolder"], self.get_selected_option())):
            showerror("Error","Selected option is a folder, not a save.")
            return
        self.location_data["savesFolder"] = os.path.join(self.location_data["savesFolder"], self.get_selected_option())
        self.refresh_saves()

    # Saves List - Goes back a folder
    def back_folder(self):
        if self.location_data["savesFolder"] == self.location_data["savesFolderCONST"]: return
        self.location_data["savesFolder"] = os.path.dirname(self.location_data["savesFolder"])
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
        items_for_saves = self.get_saves(self.location_data["savesFolder"])
        for items in items_for_saves:
            self.saves_list.insert(END,items)

    # Backs up the current save as specified name
    def backup_save(self, new_name:str):
        if not os.path.isdir(loc+f"\\Saves\\{new_name}"):
            os.makedirs(loc+f"\\Saves\\{new_name}")

        save_file(loc+f"\\Saves\\{new_name}\\file0",open_file(self.location_data["data"] + "\\file0"))
        save_file(loc+f"\\Saves\\{new_name}\\file9",open_file(self.location_data["data"] + "\\file9"))
        save_file(loc+f"\\Saves\\{new_name}\\file8",open_file(self.location_data["data"] + "\\file8"))
        save_file(loc+f"\\Saves\\{new_name}\\undertale.ini",open_file(self.location_data["data"] + "\\undertale.ini"))
        print(f"\nSave backed up as '{new_name}'\n")

    # Presents a GUI for backing up the current save
    def backup_save_gui(self):
        new_save = askstring("Backup","Please enter a name for the new save. Seperate folders with \\\\")
        if new_save != None:
            self.backup_save(new_save)
            showinfo("Success",f"Your Save, '{new_save}' has been backed up.")

    # Writes specified backup to the current save
    def write_save(self, backup_name:str):
        try_to_delete(self.location_data["data"] + "\\file0")
        try_to_delete(self.location_data["data"] + "\\file9")
        try_to_delete(self.location_data["data"] + "\\undertale.ini")
        try_to_delete(self.location_data["data"] + "\\file8")
        
        save_file(self.location_data["data"] + "\\file0",open_file(self.location_data["savesFolder"] + f"\\{backup_name}\\file0"))
        save_file(self.location_data["data"] + "\\file9",open_file(self.location_data["savesFolder"] + f"\\{backup_name}\\file9"))
        save_file(self.location_data["data"] + "\\file8",open_file(self.location_data["savesFolder"] + f"\\{backup_name}\\file8"))
        save_file(self.location_data["data"] + "\\undertale.ini",open_file(self.location_data["savesFolder"] + f"\\{backup_name}\\undertale.ini"))

    # Presents a GUI for writing a backup to the current save
    def write_save_gui(self):
        # Check if the selected save is a folder or a save
        if not self.is_save(os.path.join(self.location_data["savesFolder"], self.get_selected_option())):
            showerror("Error","You can't load a folder.")
            return

        data = self.location_data["data"]
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

    # Gets all the saves in a folder (for the saves list)
    def get_saves(self, path:str):
        saves = os.listdir(path)
        for i in range(len(saves)):
            if not self.is_save(f"{self.location_data["savesFolder"]}\\{saves[i]}"): saves[i] = "  [Folder] " + saves[i]
            else: saves[i] = "  [Save] " + saves[i]
        return saves

if __name__ == "__main__":
    loc = get_current_dir()
    w = UndertaleSaveManager()
    w.mainloop()
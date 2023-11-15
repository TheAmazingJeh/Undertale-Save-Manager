from tkinter import *
import os, sys, ctypes
from tkinter.messagebox import  askyesnocancel, showinfo, showerror, showwarning
from tkinter.simpledialog import askstring
try:
    import pyi_splash
except ImportError:
    pass

if getattr(sys, 'frozen', False):
    loc = os.path.dirname(sys.executable)
    os.chdir(loc)
else:
    loc = os.path.dirname(os.path.realpath(__file__))

location_data = {
    "exe":"C:\\Program Files (x86)\\Steam\\steamapps\\common\\Undertale",
    "data":os.getenv("LOCALAPPDATA")+"\\UNDERTALE",
    "savesFolder": loc+"\\Saves",
    "savesFolderCONST": loc+"\\Saves"
}

def close_splash(): # Closes the splash screen, if it exists
    try:
        pyi_splash.close()
    except NameError:
        pass

if not os.path.exists(location_data["data"]): # 
    close_splash()
    showerror("Error","No save file found.\nPlease make sure you have installed Undertale & have ran it at least once.")
    sys.exit()
if not os.path.exists(loc+"\\Saves"):
    os.makedirs(loc+"\\Saves")

def open_file(file_name): # Opens a file
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

def is_save(path): # Returns True if a directory has files in it
    f = []
    for (dirpath, dirnames, filenames) in os.walk(path):
        f.extend(filenames)
        break
    if len(f) > 0:
        return True
    else:
        return False

def backup_save(new_name): # Backs up the current save
    if not os.path.isdir(loc+f"\\Saves\\{new_name}"):
        os.makedirs(loc+f"\\Saves\\{new_name}")

    save_file(loc+f"\\Saves\\{new_name}\\file0",open_file(location_data["data"] + "\\file0"))
    save_file(loc+f"\\Saves\\{new_name}\\file9",open_file(location_data["data"] + "\\file9"))
    save_file(loc+f"\\Saves\\{new_name}\\file8",open_file(location_data["data"] + "\\file8"))
    save_file(loc+f"\\Saves\\{new_name}\\undertale.ini",open_file(location_data["data"] + "\\undertale.ini"))
    print(f"\nSave backed up as '{new_name}'\n")

def get_saves(path):
    saves = os.listdir(path)
    for i in range(len(saves)):
        if not is_save(f"{location_data["savesFolder"]}\\{saves[i]}"): saves[i] = "[Folder] " + saves[i]
        else: saves[i] = "[Save] " + saves[i]
    return saves

def write_save(backup_name):
    try_to_delete(location_data["data"] + "\\file0")
    try_to_delete(location_data["data"] + "\\file9")
    try_to_delete(location_data["data"] + "\\undertale.ini")
    try_to_delete(location_data["data"] + "\\file8")
    
    save_file(location_data["data"] + "\\file0",open_file(location_data["savesFolder"] + f"\\{backup_name}\\file0"))
    save_file(location_data["data"] + "\\file9",open_file(location_data["savesFolder"] + f"\\{backup_name}\\file9"))
    save_file(location_data["data"] + "\\file8",open_file(location_data["savesFolder"] + f"\\{backup_name}\\file8"))
    save_file(location_data["data"] + "\\undertale.ini",open_file(location_data["savesFolder"] + f"\\{backup_name}\\undertale.ini"))

def write_save_gui():
    # Check if the selected save is a folder or a save
    if not is_save(os.path.join(location_data["savesFolder"], GetSelectedSave())):
        showerror("Error","You can't load a folder.")
        return

    data = location_data["data"]
    if os.path.exists(f"{data}\\undertale.ini"):
        oversave = askyesnocancel("Warning","A save already exists. Do you want to overwrite it?")
        if oversave == False:
            new_save = askstring("Backup","Please enter a name for the old save, so it can be backed up.")
            if new_save != None:
                backup_save(new_save)
            else:
                return
        if oversave != True and oversave != False:
            return
        write_save(GetSelectedSave())
        showinfo("Success",f"Your Save, '{GetSelectedSave()}' has been loaded.")

def backup_save_gui():
    new_save = askstring("Backup","Please enter a name for the new save. Seperate folders with \\\\")
    if new_save != None:
        backup_save(new_save)
        showinfo("Success",f"Your Save, '{new_save}' has been backed up.")

def open_folder():
    if is_save(os.path.join(location_data["savesFolder"], GetSelectedSave())):
        showerror("Error","Selected option is a folder, not a save.")
        return
    location_data["savesFolder"] = os.path.join(location_data["savesFolder"], GetSelectedSave())
    refresh_saves(location_data["savesFolder"])

def back_folder():
    if location_data["savesFolder"] == location_data["savesFolderCONST"]: return
    location_data["savesFolder"] = os.path.dirname(location_data["savesFolder"])
    refresh_saves(location_data["savesFolder"])

def setwindowmiddle(wd,width, height):
    user32 = ctypes.windll.user32
    screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1) # Multi Monitor Fix
    middle = screensize[0] // 2, screensize[1] // 2
    add = middle[0] - width // 2, middle[1] - height // 2
    wd.geometry(f"{width}x{height}+{add[0]}+{add[1]}")

w = Tk()
w.title("Save Manager")
if os.path.exists(loc+"\\UNDERTALE.ico"):
    w.iconbitmap(loc+"\\UNDERTALE.ico")
    
w.configure()
setwindowmiddle(w,469,165)
w.resizable(False, False)

def GetSelectedSave():
    value=str((saves_list.get(ACTIVE)))
    value = value.replace("[Save]","")
    value = value.replace("[Folder]","")
    value = value.strip()
    return value

def refresh_saves(path):
    saves_list.delete(0,END)
    items_for_saves = get_saves(path)
    for items in items_for_saves:
        saves_list.insert(END,items)

Button(w, text="Backup Loaded Save", command=backup_save_gui).grid(row=0, column=1, sticky=N, columnspan=2)
Button(w, text="Load Selected Save", command=write_save_gui).grid(row=1, column=1, sticky=N, columnspan=2)
Button(w, text="Refresh Saves List", command=lambda: refresh_saves(location_data["savesFolder"])).grid(row=2, column=1, sticky=N, columnspan=2)
Button(w, text="Open Folder", command=open_folder).grid(row=3, column=1, sticky=N)
Button(w, text="Back", command=back_folder).grid(row=3, column=2, sticky=N)
Button(w, text="Quit", command=sys.exit).grid(row=4, column=1, sticky=N, columnspan=2)

saves_list = Listbox(w, height=10, width=50)
saves_list.grid(row=0, column=3, rowspan=5)

scrollbar = Scrollbar(w)
scrollbar.grid(row=0, column=4,rowspan=5, sticky=N+S)

saves_list.config(yscrollcommand = scrollbar.set)
scrollbar.config(command = saves_list.yview)

refresh_saves(location_data["savesFolder"])

close_splash()

w.mainloop()
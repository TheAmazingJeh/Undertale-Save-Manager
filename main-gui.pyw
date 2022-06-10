from tkinter import *
import os, sys
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
    "data":os.getenv("LOCALAPPDATA")+"\\UNDERTALE"
}

def close_splash():
    try:
        pyi_splash.close()
    except NameError:
        pass

if not os.path.exists(location_data["data"]):
    close_splash()
    showerror("Error","No save file found.\nPlease make sure you have installed Undertale.")
    sys.exit()
if not os.path.exists(loc+"\\Saves"):
    close_splash()
    showerror("Error","No save folder exists. Please add one before running this program.")
    sys.exit()

def open_file(file_name):      
    try:
        with open(file_name, 'r') as file:
            return file.read()
    except FileNotFoundError:
        return ""

def save_file(file_name, data):
    with open(file_name, 'w') as file:
        file.write(data)

def try_to_delete(file_name):
    try:
        os.remove(file_name)
    except FileNotFoundError:
        pass

def backup_save(new_name):
    if not os.path.isdir(loc+f"\\Saves\\{new_name}"):
        os.makedirs(loc+f"\\Saves\\{new_name}")

    save_file(loc+f"\\Saves\\{new_name}\\file0",open_file(location_data["data"] + "\\file0"))
    save_file(loc+f"\\Saves\\{new_name}\\file9",open_file(location_data["data"] + "\\file9"))
    save_file(loc+f"\\Saves\\{new_name}\\file8",open_file(location_data["data"] + "\\file8"))
    save_file(loc+f"\\Saves\\{new_name}\\undertale.ini",open_file(location_data["data"] + "\\undertale.ini"))
    print(f"\nSave backed up as '{new_name}'\n")

def get_saves():
    saves = os.listdir(loc+"\\Saves")
    return saves

def write_save(backup_name):
    try_to_delete(location_data["data"] + "\\file0")
    try_to_delete(location_data["data"] + "\\file9")
    try_to_delete(location_data["data"] + "\\undertale.ini")
    try_to_delete(location_data["data"] + "\\file8")
    
    save_file(location_data["data"] + "\\file0",open_file(loc+f"\\Saves\\{backup_name}\\file0"))
    save_file(location_data["data"] + "\\file9",open_file(loc+f"\\Saves\\{backup_name}\\file9"))
    save_file(location_data["data"] + "\\file8",open_file(loc+f"\\Saves\\{backup_name}\\file8"))
    save_file(location_data["data"] + "\\undertale.ini",open_file(loc+f"\\Saves\\{backup_name}\\undertale.ini"))

def write_save_gui():
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
    new_save = askstring("Backup","Please enter a name for the new save.")
    if new_save != None:
        backup_save(new_save)
        showinfo("Success",f"Your Save, '{new_save}' has been backed up.")

w = Tk()
w.title("Save Manager")
if os.path.exists(loc+"\\UNDERTALE.ico"):
    w.iconbitmap(loc+"\\UNDERTALE.ico")
    
w.configure()
w.eval('tk::PlaceWindow . centre')
w.resizable(False, False)

def GetSelectedSave():
    value=str((saves_list.get(ACTIVE)))
    return value

def refresh_saves():
    saves_list.delete(0,END)
    items_for_saves = get_saves()
    for items in items_for_saves:
        saves_list.insert(END,items)

Label(w, text="   ").grid(row=0, column=0)
Button(w, text="Backup Loaded Save", command=backup_save_gui).grid(row=0, column=1, sticky=N)
Button(w, text="Load Selected Save", command=write_save_gui).grid(row=1, column=1, sticky=N)
Button(w, text="Refresh Saves List", command=refresh_saves).grid(row=2, column=1, sticky=N)
Button(w, text="Quit", command=sys.exit).grid(row=3, column=1, sticky=N)
Label(w, text="   ").grid(row=0, column=2)

saves_list = Listbox(w, height=10, width=50)
saves_list.grid(row=0, column=3, rowspan=5)

scrollbar = Scrollbar(w)
scrollbar.grid(row=0, column=4,rowspan=5, sticky=N+S)

saves_list.config(yscrollcommand = scrollbar.set)
scrollbar.config(command = saves_list.yview)

refresh_saves()

close_splash()

w.mainloop()
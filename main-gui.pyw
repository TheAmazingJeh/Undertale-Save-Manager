from tkinter import *
import os
from tkinter.messagebox import  askyesnocancel, showinfo
from tkinter.simpledialog import askstring

from main import *
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
w.configure()
w.resizable(False, False)


def GetSelectedSave():
    value=str((saves_list.get(ACTIVE)))
    return value

def refresh_saves():
    saves_list.delete(0,END)
    items_for_saves = get_saves()
    for items in items_for_saves:
        saves_list.insert(END,items)

Button(w, text="Backup Loaded Save", command=backup_save_gui).grid(row=0, column=0)
Button(w, text="Load Selected Save", command=write_save_gui).grid(row=1, column=0)
Button(w, text="Refresh Saves List", command=refresh_saves).grid(row=2, column=0)
Button(w, text="Quit", command=quit).grid(row=3, column=0)
Label(w, text="   ").grid(row=0, column=1)


saves_list = Listbox(w, height=10, width=50)
saves_list.grid(row=0, column=2, rowspan=5)

refresh_saves()

w.mainloop()
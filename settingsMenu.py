import os
import json
from tkinter import Button, Frame, LEFT, ACTIVE
from tkinter.simpledialog import Dialog

class Settings(Dialog):
    def __init__(self, parent, loc, cfg):
        self.parent = parent
        self.loc = loc
        self.file_config = cfg
        super().__init__(parent)

    def reset_game_launch(self):
        if "GAMETYPE" in self.file_config:
            del self.file_config["GAMETYPE"]
            with open(os.path.join(self.loc, "config.json"), 'w') as f:
                json.dump(self.file_config, f, indent=4)

    def open_saves_folder(self):
        os.startfile(self.file_config["savesFolder"])

    def open_active_save_folder(self):
        os.startfile(self.file_config["data"])

    def body(self, master):
        self.minsize(width=250, height=10)
        Button(master, text="Reset Game Launch Type", command=self.reset_game_launch).grid(row=0)
        Button(master, text="Open Undertale Saves Folder", command=self.open_saves_folder).grid(row=1)
        Button(master, text="Open Active Save Folder", command=self.open_active_save_folder).grid(row=2)
    
    def buttonbox(self):
        box = Frame(self)
        w = Button(box, text="Back", width=10, command=self.ok, default=ACTIVE)
        w.pack(side=LEFT, padx=5, pady=5)
        self.bind("<Return>", self.ok)
        box.pack()
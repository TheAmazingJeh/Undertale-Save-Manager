import os
import json
from tkinter import Button, Frame, LEFT, ACTIVE
from tkinter.simpledialog import Dialog

# Creates a dialog box that allows the user to change settings
class Settings(Dialog):
    # Initialize the dialog
    def __init__(self, parent, loc, cfg):
        # Set the parent window
        self.parent = parent
        # Set the base location of the file
        self.loc = loc
        # Set the config file
        self.file_config = cfg
        # Initialize the dialog
        super().__init__(parent)

    # Function to reset the game launch type
    def reset_game_launch(self):
        # Check if the game launch type is in the config file
        if "GAMETYPE" in self.file_config:
            # Delete the game launch type from the config file
            del self.file_config["GAMETYPE"]
            # Write the config file
            with open(os.path.join(self.loc, "config.json"), 'w') as f:
                json.dump(self.file_config, f, indent=4)

    # Function to open the Undertale saves folder
    def open_saves_folder(self):
        os.startfile(self.file_config["savesFolder"])

    # Function to open the active save folder
    def open_active_save_folder(self):
        os.startfile(self.file_config["data"])

    # Function to create the body of the dialog
    def body(self, master):
        # Set the minimum size of the dialog
        self.minsize(width=250, height=10)
        # Button to reset the game launch type
        Button(master, text="Reset Game Launch Type", command=self.reset_game_launch).grid(row=0)
        # Button to open the Undertale saves folder
        Button(master, text="Open Undertale Saves Folder", command=self.open_saves_folder).grid(row=1)
        # Button to open the active save folder
        Button(master, text="Open Active Save Folder", command=self.open_active_save_folder).grid(row=2)
    
    # Function to create the button box
    def buttonbox(self):
        # Create the button box
        box = Frame(self)
        # Button to close the dialog
        w = Button(box, text="Back", width=10, command=self.ok, default=ACTIVE)
        # Pack the button
        w.pack(side=LEFT, padx=5, pady=5)
        # Bind the enter key to the button
        self.bind("<Return>", self.ok)
        # Pack the button box
        box.pack()
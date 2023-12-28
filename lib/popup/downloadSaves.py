from tkinter.simpledialog import Dialog
from tkinter import Frame, Button, Listbox, Scrollbar
from tkinter.messagebox import showerror

import requests

from urllib import request
import os, json, base64

def internet_on():
    try:
        request.urlopen('http://google.com', timeout=5)
        return True
    except request.URLError as err: 
        return False


# Class to select the type of game to open
class ExampleSaves(Dialog):
    def __init__(self, parent, file_location, title="Example Saves"):
        # Set the base location of the file
        self.loc = file_location
        self.saves_path = os.path.join(self.loc, "Example Saves")
        self.download_url = "https://raw.githubusercontent.com/TheAmazingJeh/TheAmazingJeh.github.io/master/files/save_files/undertale/undertale.json"
        self.saves_dict = {}

        if not os.path.exists(self.saves_path):
            os.mkdir(self.saves_path)


        # Initialize the dialog
        super().__init__(parent, title)

    # Function to create the body of the dialog
    def body(self, master):
        # Set the minimum size of the dialog
        self.minsize(width=250, height=100)
        self.place_widgets()

    def place_widgets(self):
        self.top_frame = Frame(self)
        self.get_saves = Button(self.top_frame, text="Download All Saves (0.5 mbs)", command=self.download_saves)
        self.get_saves.pack(side="top", anchor="n", padx=5, pady=5)
        self.top_frame.pack(side="top", fill="x", expand=True)

        self.list_box_frame = Frame(self)
        self.saves = Listbox(self.list_box_frame)
        self.saves.pack(side="left", fill="both", expand=True)
        self.saves_scrollbar = Scrollbar(self.list_box_frame)
        self.saves_scrollbar.pack(side="right", fill="y")
        self.saves.config(yscrollcommand=self.saves_scrollbar.set)
        self.saves_scrollbar.config(command=self.saves.yview)
        self.list_box_frame.pack(side="top", fill="both", expand=True)

        # Make frame above buttons
        self.button_frame = Frame(self)
        self.load_all_saves = Button(self.button_frame, text="Load All Saves", command=self.load_all_saves)
        self.load_all_saves.pack(side="top", pady=5)
        self.button_frame.pack(side="top", fill="x", expand=True)

        self.fill_saves_list()

    def fill_saves_list(self):
        if not os.path.exists(os.path.join(self.saves_path, "undertale.json")):
            self.saves.insert("end", "Please download all saves first")
        else:
            with open(os.path.join(self.saves_path, "undertale.json"), "r") as f:
                self.saves_dict = json.load(f)
                for save_name in self.saves_dict.keys():
                    self.saves.insert("end", save_name.replace("_", "'"))
        
        # Set the default selection to the first item in the list
        self.saves.select_set(0)

    def clear_saves_list(self):
        self.saves.delete(0, "end")

    def download_saves(self):
        # Check if internet is on
        if not internet_on():
            showerror("Error", "No internet connection")
            return
        # Download the saves
        r = requests.get(self.download_url)
        with open(os.path.join(self.saves_path, "undertale.json"), "wb") as f:
            f.write(r.content)
        # Clear the list
        self.clear_saves_list()
        # Fill the list
        self.fill_saves_list()

    def load_save_from_base64(self, save_name):
        with open(os.path.join(self.saves_path, "undertale.json"), "r") as f:
            save_data = json.load(f)
        if save_name in self.saves_dict.keys():
            data = save_data[save_name]
            
            # Make save folder
            save_folder = os.path.join(self.loc, "Saves", "Example", save_name)
            if not os.path.exists(save_folder):
                os.makedirs(save_folder)
            
            # Make all files in save folder
            for file_name in data.keys():
                file_path = os.path.join(save_folder, file_name)
                with open(file_path, "wb") as f:
                    f.write(base64.b64decode(data[file_name]))
            return True
            
        else:
            showerror("Error", "Save not in list of saves.")
            return False

    def load_all_saves(self):
        for save_name in self.saves_dict.keys():
            self.load_save_from_base64(save_name.replace("'", "_"))
        self.destroy()

    # Function to validate the input
    def validate(self):
        # Get text value of the selected item
        self.result = self.saves.get(self.saves.curselection())
        if self.result == "Please download all saves first" or self.result == None:
            return False
        return True

    # Function that is called when the dialog is closed
    def apply(self):
        save_name = self.saves.get(self.saves.curselection()).replace("'", "_")
        return self.load_save_from_base64(save_name)
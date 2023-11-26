from tkinter import DISABLED, NORMAL, StringVar, W, Button, Entry, IntVar, Label, Radiobutton
from tkinter.filedialog import askopenfilename
from tkinter.simpledialog import Dialog

from tkinter import Tk

# Class to select the type of game to open
class GameTypeSelect(Dialog):
    def __init__(self, parent, file_location, title=None):
        # Initialize the dialog
        super().__init__(parent, title)
        # Set the base location of the file
        self.loc = file_location

    # Function to select the type of game to open
    def sel(self):
        # Get the selected option
        match self.radioVar.get():
            # If the option is 1, disable the file select button and entry
            case 1: 
                self.file_select.config(state=DISABLED)
                self.file_label_truncated.config(state=DISABLED)
            # If the option is 2, enable the file select button and entry
            case 2: 
                self.file_select.config(state=NORMAL)
                self.file_label_truncated.config(state=DISABLED)

    def select_file(self):
        # Open a file dialog to select the file, starting in the game's directory and only showing executables
        self.fileName = askopenfilename(initialdir="C:\\Program Files (x86)\\Steam\\steamapps\\common\\UNDERTALE", filetypes=[("Executable", "*.exe")])
        # Set the preview text to the file name, truncated to 32 characters
        self.file_string_truncated.set("..."+self.fileName[-32:])

    # Function to create the body of the dialog
    def body(self, master):
        # Set the minimum size of the dialog
        self.minsize(width=250, height=100)
        # Set the result to an empty string
        self.fileName = ""
        # Label to tell the user to select an option
        Label(master,text="Please select an option.").grid(sticky=W)

        # Radio buttons to select option 1, open the game by using Steam.
        self.radioVar = IntVar()
        self.r1 = Radiobutton(master, text="Open By Using Steam Link", variable=self.radioVar, value=1,command=self.sel)
        self.r1.grid(row=1, sticky=W)

        # Radio buttons to select option 2, open the game by directly running the file.
        self.r2 = Radiobutton(master, text="Open By Directly Running File", variable=self.radioVar, value=2,command=self.sel)
        self.r2.grid(row=2, sticky=W)
        self.file_select = Button(master, text="Select File", command=self.select_file)
        self.file_select.grid(row=2,column=1, sticky=W)

        # Entry to show the file name, truncated to 32 characters
        self.file_string_truncated = StringVar()
        self.file_label_truncated = Entry(master, textvariable=self.file_string_truncated, width=40)
        self.file_label_truncated.grid(row=3,column=0, columnspan=2,sticky=W, pady=5)

        # Set the default option to 1
        self.r1.invoke()
    
    # Function that is called when the dialog is closed
    def apply(self):
        # Get the selected option
        match self.radioVar.get():
            # If the option is 1, set the result to open the game by using Steam, with the game ID for Undertale
            case 1: 
                self.result = ["Steam","start \"\" steam://rungameid/391540"]
            # If the option is 2, set the result to open the game by directly running the file, with the file path
            case 2: 
                self.fileName = f'explorer.exe "{self.loc}"' if self.fileName == "" else f'"{self.fileName}"'
                self.result = ["Direct",self.fileName]
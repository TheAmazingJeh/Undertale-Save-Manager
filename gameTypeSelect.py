from tkinter import DISABLED, NORMAL, StringVar, W, Button, Entry, IntVar, Label, Radiobutton
from tkinter.filedialog import askopenfilename
from tkinter.simpledialog import Dialog

from tkinter import Tk

class GameTypeSelect(Dialog):
    def __init__(self, parent, file_location, title=None):
        super().__init__(parent, title)
        self.loc = file_location

    def sel(self):
        match self.radioVar.get():
            case 1: self.file_select.config(state=DISABLED), self.file_label_truncated.config(state=DISABLED)
            case 2: self.file_select.config(state=NORMAL), self.file_label_truncated.config(state=DISABLED)
    def select_file(self):
        self.fileName = askopenfilename(initialdir="C:\\Program Files (x86)\\Steam\\steamapps\\common\\UNDERTALE", filetypes=[("Executable", "*.exe")])
        self.file_string_truncated.set("..."+self.fileName[-32:])
    def body(self, master):
        self.minsize(width=250, height=100)
        self.fileName = ""
        Label(master,text="Please select an option.").grid(sticky=W)

        self.radioVar = IntVar()
        self.r1 = Radiobutton(master, text="Open By Using Steam Link", variable=self.radioVar, value=1,command=self.sel)
        self.r1.grid(row=1, sticky=W)

        self.r2 = Radiobutton(master, text="Open By Directly Running File", variable=self.radioVar, value=2,command=self.sel)
        self.r2.grid(row=2, sticky=W)
        self.file_select = Button(master, text="Select File", command=self.select_file)
        self.file_select.grid(row=2,column=1, sticky=W)

        self.file_string_truncated = StringVar()
        self.file_label_truncated = Entry(master, textvariable=self.file_string_truncated, width=40)
        self.file_label_truncated.grid(row=3,column=0, columnspan=2,sticky=W, pady=5)

        self.r1.invoke()
    
    def apply(self):
        match self.radioVar.get():
            case 1: 
                self.result = ["Steam","start \"\" steam://rungameid/391540"]
            case 2: 
                self.fileName = f'explorer.exe "{self.loc}"' if self.fileName == "" else f'"{self.fileName}"'
                self.result = ["Direct",self.fileName]
        return
    

if __name__ == "__main__":
    root = Tk()
    root.withdraw()
    print(GameTypeSelect(root,"C:\\Users\\joehb\\Documents\\Coding\\Personal-Python\\Games\\Toby Fox Saves Manager\\Undertale-Save-Manager").result)
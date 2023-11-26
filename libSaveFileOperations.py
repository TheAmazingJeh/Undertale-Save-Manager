import os

from libBasicFileFunctions import open_file, save_file

# Backs up the current save as specified name
def backup_save(new_name:str, program_data:dict, loc:str):
    # If the saves folder doesn't exist, create it
    if not os.path.isdir(loc+f"\\Saves\\{new_name}"):
        os.makedirs(loc+f"\\Saves\\{new_name}")

    # Backup the save by copying all 4 files from the data folder to the new save folder
    save_file(loc+f"\\Saves\\{new_name}\\file0",open_file(program_data["data"] + "\\file0"))
    save_file(loc+f"\\Saves\\{new_name}\\file9",open_file(program_data["data"] + "\\file9"))
    save_file(loc+f"\\Saves\\{new_name}\\file8",open_file(program_data["data"] + "\\file8"))
    save_file(loc+f"\\Saves\\{new_name}\\undertale.ini",open_file(program_data["data"] + "\\undertale.ini"))
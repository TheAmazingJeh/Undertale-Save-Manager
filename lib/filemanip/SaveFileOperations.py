import os

from lib.BasicFileFunctions import open_file, save_file, try_to_delete

# Backs up the current save as specified name
def backup_save(new_name:str, program_data:dict, loc:str):
    # If the saves folder doesn't exist, create it
    if not os.path.isdir(os.path.join(loc, "Saves", new_name)):
        os.makedirs(os.path.join(loc, "Saves", new_name))

    # Backup the save by copying all 4 files from the data folder to the new save folder
    save_file(os.path.join(loc, "Saves", new_name, "file0"), open_file(os.path.join(program_data["data"], "file0")))
    save_file(os.path.join(loc, "Saves", new_name, "file9"), open_file(os.path.join(program_data["data"], "file9")))
    save_file(os.path.join(loc, "Saves", new_name, "file8"), open_file(os.path.join(program_data["data"], "file8")))
    save_file(os.path.join(loc, "Saves", new_name, "undertale.ini"), open_file(os.path.join(program_data["data"], "undertale.ini")))

# Writes specified backup to the current save
def write_save(backup_name:str, program_data:dict):
    try_to_delete(os.path.join(program_data["data"], "file0"))
    try_to_delete(os.path.join(program_data["data"], "file8"))
    try_to_delete(os.path.join(program_data["data"], "file9"))
    try_to_delete(os.path.join(program_data["data"], "undertale.ini"))
    
    save_file(os.path.join(program_data["data"], "file0"), open_file(os.path.join(program_data["savesFolder"], backup_name, "file0")))
    save_file(os.path.join(program_data["data"], "file8"), open_file(os.path.join(program_data["savesFolder"], backup_name, "file8")))
    save_file(os.path.join(program_data["data"], "file9"), open_file(os.path.join(program_data["savesFolder"], backup_name, "file9")))
    save_file(os.path.join(program_data["data"], "undertale.ini"), open_file(os.path.join(program_data["savesFolder"], backup_name, "undertale.ini")))
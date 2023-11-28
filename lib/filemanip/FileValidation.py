import os

# Checks if a directory is a save or not
def is_save(path:str):
    f = []
    # Get the files in the directory
    for (dirpath, dirnames, filenames) in os.walk(path):
        f.extend(filenames)
        break
    # If the directory contains any files, it's a save
    if len(f) > 0:
        return True
    else:
        return False

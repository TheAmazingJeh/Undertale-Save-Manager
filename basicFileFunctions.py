import os

# Opens a file and returns the contents as a string
def open_file(file_name): 
    try:
        with open(file_name, 'r') as file:
            return file.read()
    except FileNotFoundError:
        return ""

# Saves a file, overwriting the contents
def save_file(file_name, data): 
    with open(file_name, 'w') as file:
        file.write(data)

# Tries to delete a file, but doesn't error if it doesn't exist
def try_to_delete(file_name):
    try:
        os.remove(file_name)
    except FileNotFoundError:
        pass
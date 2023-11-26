import os
    
def open_file(file_name): 
    try:
        with open(file_name, 'r') as file:
            return file.read()
    except FileNotFoundError:
        return ""

def save_file(file_name, data): # Saves a file
    with open(file_name, 'w') as file:
        file.write(data)

def try_to_delete(file_name): # Tries to delete a file, but doesn't error if it doesn't exist
    try:
        os.remove(file_name)
    except FileNotFoundError:
        pass
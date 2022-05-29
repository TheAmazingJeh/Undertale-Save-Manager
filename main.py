import os

loc = os.path.dirname(os.path.realpath(__file__))
location_data = {
    "exe":"C:\\Program Files (x86)\\Steam\\steamapps\\common\\Undertale",
    "data":os.getenv("LOCALAPPDATA")+"\\UNDERTALE"
}
def open_file(file_name):      
    try:
        with open(file_name, 'r') as file:
            return file.read()
    except FileNotFoundError:
        return ""

def save_file(file_name, data):
    with open(file_name, 'w') as file:
        file.write(data)

def try_to_delete(file_name):
    try:
        os.remove(file_name)
    except FileNotFoundError:
        pass

def backup_save(new_name):
    if not os.path.isdir(loc+f"\\Saves\\{new_name}"):
        os.makedirs(loc+f"\\Saves\\{new_name}")

    save_file(loc+f"\\Saves\\{new_name}\\file0",open_file(location_data["data"] + "\\file0"))
    save_file(loc+f"\\Saves\\{new_name}\\file9",open_file(location_data["data"] + "\\file9"))
    save_file(loc+f"\\Saves\\{new_name}\\file8",open_file(location_data["data"] + "\\file8"))
    save_file(loc+f"\\Saves\\{new_name}\\undertale.ini",open_file(location_data["data"] + "\\undertale.ini"))
    print(f"\nSave backed up as '{new_name}'\n")

def write_save(backup_name):
    if not os.path.exists(loc+f"\\Saves\\{backup_name}"):
        print("No save with that name was found\n")
        return
    data = location_data["data"]
    if os.path.exists(f"{data}\\undertale.ini"):
        oversave = input("A save already exists. Do you want to overwrite it? (y/n) >>>   ")
        if oversave == "n":
            backup_save(input("Please enter a name for the old save >>>   "))

    try_to_delete(location_data["data"] + "\\file0")
    try_to_delete(location_data["data"] + "\\file9")
    try_to_delete(location_data["data"] + "\\undertale.ini")
    try_to_delete(location_data["data"] + "\\file8")
    
    save_file(location_data["data"] + "\\file0",open_file(loc+f"\\Saves\\{backup_name}\\file0"))
    save_file(location_data["data"] + "\\file9",open_file(loc+f"\\Saves\\{backup_name}\\file9"))
    save_file(location_data["data"] + "\\file8",open_file(loc+f"\\Saves\\{backup_name}\\file8"))
    save_file(location_data["data"] + "\\undertale.ini",open_file(loc+f"\\Saves\\{backup_name}\\undertale.ini"))
    print(f"\nSave '{backup_name}' loaded\n")
    
def list_saves():
    saves = os.listdir(loc+"\\Saves")
    print("\n")
    for i in range(len(saves)):
        print(f"• {saves[i]}")
    print("\n")

if __name__ == "__main__":
    while True:
        print("""
    1. Backup Loaded Save
    2. Load New Save
    3. List All Saves
    4. Exit
""")
        choice = input("Please enter your choice >>>   ")
        if choice == "1":
            backup_save(input("Please enter a name for the save >>>   "))
        elif choice == "2":
            write_save(input("Please enter the name of the save to write >>>   "))
        elif choice == "3":
            list_saves()
            input("Press enter to continue >>>   ")
        elif choice == "4":
            break
        else:
            print("Invalid choice.")
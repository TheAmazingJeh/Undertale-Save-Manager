import os, json

# Loads the config file
def load_config(loc:str):
    # If the config file doesn't exist, create it
    if not os.path.exists(os.path.join(loc, "config.json")):
        with open(os.path.join(loc, "config.json"), 'w') as f:
            defaultConfig = {
                "exe":None,
            }
            # Write the default config to the config file
            json.dump({}, f, indent=4)

    # Load the config file
    with open(os.path.join(loc, "config.json"), 'r') as f:
        # Set the config file to a variable
        vars = json.load(f)
        saveFlag = False
        # If the exe isn't in the config file, set it to None and save the config file
        if "exe" not in vars:
            vars["exe"] = None
            saveFlag = True
        # If the config has changed, save the config file
        if saveFlag:
            with open(os.path.join(loc, "config.json"), 'w') as f:
                json.dump(vars, f, indent=4)
    # Return the config file
    return vars

# Saves the config file
def save_config(loc, program_data):
    # Save the config file
    with open(os.path.join(loc, "config.json"), 'w') as f:
        json.dump(program_data, f, indent=4)
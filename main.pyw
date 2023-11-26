from undertaleSaveManager import UndertaleSaveManager

# Tries to import the splash screen, but doesn't error if it doesn't exist (for pyinstaller)
try: 
    import pyi_splash
except ImportError:
    pass

# Closes the splash screen, if it exists (for pyinstaller)
def close_splash(): 
    try:
        pyi_splash.close()
    except NameError:
        pass

if __name__ == "__main__":
    w = UndertaleSaveManager()
    w.mainloop()
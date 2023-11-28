import sys, os

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

def get_icon():
    if getattr(sys, 'frozen', False):
        # If the program is running as a pyinstaller executable, return the icon as a base64 string
        icon = ["base64", "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAEuSURBVDhPjZJBEsIwDAOd3PgAB/7/R24NWskpMMAMgklsRbbVtKMaR9UalXQQfsHiP3SqeK5ovPiAnYxI+5QUbuOooWPLBKJVU8FkMjTFQwFVSCmwVjhsadVxuylwIpE0Y6w5FJDw240iOOvd0J3v9xAND7S1FmMFXVZMdp7U019BmRwg5CAugEvtClprOxhMuF6rLhdxtFelnzV/T7AofTg/Nyj30eKRiuF1kVFZ5KVPgBux9MV5t8gae87scLEV2A2qrVcH93CliXYEk9xCizwOAuTtJE8TXPjNpDTwl6jsRWb+ubUDNOJmpoQD+12ufYldGETW1+ddzHuDDdV1h86Q902R8fn6qKH8HYhsjgo9U24d3qTjv8BAvhHv+x6/4MPBCQ3zpfI6f5ZXPQD+ZpZ2O7kaKQAAAABJRU5ErkJggg=="]
    else:
        # If the program is running as a python script, return the icon as a file path
        icon = ["path", "UNDERTALE.ico"]

    return icon
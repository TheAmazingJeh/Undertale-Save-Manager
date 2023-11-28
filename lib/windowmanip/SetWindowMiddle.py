import ctypes

# Sets the window to the middle of the screen
def set_window_middle(window, width:int, height:int):
    # Get the current user
    user32 = ctypes.windll.user32
    # Get the screen size, x and y
    screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    # Get the middle of the screen
    middle = screensize[0] // 2, screensize[1] // 2
    # Get the middle of the window
    add = middle[0] - width // 2, middle[1] - height // 2
    # Set the window size and position
    window.geometry(f"{width}x{height}+{add[0]}+{add[1]}")
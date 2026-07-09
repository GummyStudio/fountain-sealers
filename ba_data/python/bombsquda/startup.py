import babase as ba
import ctypes

def rename_window(text: str):
    try:
        user32 = ctypes.windll.user32
    except:
        user32 = None
    hwnd = ba.app.window_hwnd
    if not hwnd:
        return False
    user32.SetWindowTextW(hwnd, text)
    return True

class Startup():
    # check if values exist
    # global cfg
    # cfg = bui.app.config
    # made by temp in the 'bombarmy' discussion in the discord server.
    # config = bs.app.config
    # conflist = {}
    # for k,v in conflist.items():
        # config.setdefault(k, v)
    # try getting user32, but if
    # it fails assume we're on multi-platform
    # and just default
    try:
        user32 = ctypes.windll.user32
    except:
        user32 = None
    title = 'BombSquad'    
    if user32:
        hwnd = user32.FindWindowW(None, title)
    else:
        hwnd = None
    ba.app.window_hwnd = hwnd
    # for now, we just wanna rename the window for aesthetic
    rename_window('BombSquad: Fountain Sealers')





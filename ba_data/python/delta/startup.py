import bauiv1 as bui
import copy
import ctypes
import babase as ba

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
    
class Startup:
    def __init__(self):
        self.game_header = 'Chapter 1'

        config = bui.app.config


        cfg = {
            'firstLaunch': True,
            'dark_dollars': 0,


            # stats
            'STATS_freezed': 0,

            # characters
            'OWNED_roaringknight': False
        }

        if 'delta' not in config or not isinstance(config['delta'], dict):
            config['delta'] = copy.deepcopy(cfg)
        else:
           
            user_delta = config['delta']
            for key, value in cfg.items():
                user_delta.setdefault(key, value)

        
        config.apply_and_commit()

        self.store = {
            'Roaring Knight': {
                'config': 'OWNED_roaringknight',
                'description':  (
                        "* That Black Knight everyone was talking about.",
                        'suprised'
                    ),
                'cost': 5000,
            }
        }
        self.stats = {
            'dd': 'dark_dollars',
            'frozen': 'STATS_freezed',
        }        
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
        

    @property
    def gameconfig(self) -> dict:
        return bui.app.config.get('delta', {})
    
    def increase_statistic(self, stat: str, by: int = 1):
        try:
            self.gameconfig[self.stats[stat]] += by
            bui.app.config.apply_and_commit()
        except:
            pass
    
    
    

import bauiv1 as bui
import copy
class Startup:
    def __init__(self):
        
        self.game_header = 'Chapter 1'
       

        config = bui.app.config

        cfg = {
            'firstLaunch': True,
            'dark_dollars': 0,
         
        }

        if 'delta' not in config or not isinstance(config['delta'], dict):
            config['delta'] = copy.deepcopy(cfg)
        else:
           
            user_delta = config['delta']
            for key, value in cfg.items():
                user_delta.setdefault(key, value)

        # Save changes to the disk
        config.apply_and_commit()

    @property
    def gameconfig(self) -> dict:
        return bui.app.config.get('delta', {})
    

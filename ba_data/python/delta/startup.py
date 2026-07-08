import bauiv1 as bui
import copy
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

        self.store = {}
        self.stats = {
            'frozen': 'STATS_freezed'
        }

    @property
    def gameconfig(self) -> dict:
        return bui.app.config.get('delta', {})
    
    def increase_statistic(self, stat: str, by: int = 1):
        if self.stats.get(stat, None):
            return
        else:
            self.gameconfig[self.stats[stat]] += by
        bui.app.config.apply_and_commit()
    
    
    

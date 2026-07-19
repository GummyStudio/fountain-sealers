# YOU ARE NOT MEANT TO BE HERE
# BUT IF YOU INSIST
# I ONLY ASK OF ONE THING
# KEEP IT INTERESTING
# FOR THOSE LESSER THAN OF YOUR KNOWLEDGE
# KEEP YOUR PROMISE
# OR WE WON'T KEEP OURS


import bascenev1 as bs
import babase
from typing import Sequence
from bascenev1._activitytypes import JoinActivity
from bascenev1lib.actor.spaz import Spaz
from bascenev1lib.gameutils import SharedObjects

def has_it():
    return bool(babase.app.classic.startup.gameconfig.get('egg', 'nolol') is None)
    
class Session(bs.Session):
    def __init__(self):
        depsets: Sequence[bs.DependencySet] = []
        super().__init__(depsets)
        cls = JoinActivity
        cls.use_music = False
        self.setactivity(bs.newactivity(cls))
        self.getactivity()._background.handlemessage(bs.DieMessage(True))
        self.music = bs.newnode(
            'sound',
            attrs={
                'sound': bs.getsound('tool2'),
                'music': True
            }
        )
        self.image = bs.newnode(
            'image',
            attrs={
                'texture': bs.gettexture('black'),
                'fill_screen': True
            }
        )
        
    def on_activity_end(self, activity, results):
        self.music.delete()
        self.image.delete()
        self.setactivity(bs.newactivity(Activity))
        
    def on_player_request(self, player: bs.SessionPlayer) -> bool:
        if len(self.sessionplayers) == 1:
            return False
        else:
            return True
            
class Activity(bs.Activity[bs.Player, bs.Team]):
    def __init__(self, settings):
        super().__init__(settings)
        self._acquire_sound = bs.getsound('protein_acquired')
        self._kill_sound = bs.getsound('board_kill')
        self._killed_it = False
        bs.newnode(
            'sound',
            attrs={
                'sound': bs.getsound('tool'),
                'music': True
            }
        )
    def on_transition_in(self):
        super().on_transition_in()
        bs.newnode(
            'terrain',
            attrs={
                'mesh': bs.getmesh('thePadBG'),
                'lighting': False,
                'background': True,
                'color_texture': bs.gettexture('black'),
            },
        )
        bs.newnode(
            'region',
            attrs={
                'scale': (999, 0.2, 999),
                'position':(0, 0,0),
                'type': 'box',
                'materials': [
                    SharedObjects.get().collision, 
                    SharedObjects.get().footing_material
                ]
            }
        )
        self.spaz = Spaz(
            color=(0.5, 0.5, 0.5), highlight=(0.6, 0.6, 0.6),
            character='Vessel', start_invincible=False
        )
        self.spaz._stronger = True
        self.spaz._punch_cooldown = 310
        self.spaz2 = Spaz(
            character='Vessel', start_invincible=False
        )
        self.spaz2.node.impact_sounds = []
        self.spaz2.node.death_sounds = []
        self.spaz2.node.fall_sounds = []
        self.spaz2.hitpoints = 1
        self.spaz2.handlemessage(bs.StandMessage((0,0, -5)))
        self.spaz2.node.head_mesh = bs.getmesh('egg')
        self.spaz2.node.color_texture = bs.gettexture('egg4')
        self.spaz2.node.color_mask_texture = bs.gettexture('black')
        self.spaz2.node.torso_mesh = None
        self.spaz2.node.pelvis_mesh = None
        self.spaz2.node.upper_arm_mesh = None
        self.spaz2.node.forearm_mesh = None
        self.spaz2.node.hand_mesh = None
        self.spaz2.node.upper_leg_mesh = None
        self.spaz2.node.lower_leg_mesh = None
        self.spaz2.node.toes_mesh = None
        self.spaz.handlemessage(bs.StandMessage((0,0,0)))
        self.spaz.max_run_speed = 0
        self.spaz.impact_scale = 0.0
        self.spaz.max_move_speed = 0.5
        # self.spaz.node.name = bs.app.classic.startup.gameconfig["SurveyChoices"]['vessel_name'].strip().capitalize()
        # self.spaz.node.name_color = (0.5, 0.5, 0.5)
        
    def on_begin(self):
        super().on_begin()
        bs.timer(0.1, self._tick, repeat=True)
        plr = self.players[0]
        plr.actor = self.spaz
        plr.assigninput(bs.InputType.LEFT_RIGHT, self.spaz.on_move_left_right)
        plr.assigninput(bs.InputType.UP_DOWN, self.spaz.on_move_up_down)
        plr.assigninput(bs.InputType.RUN, self.spaz.on_run)
        plr.assigninput(bs.InputType.PUNCH_PRESS, self.spaz.on_punch_press)
        plr.assigninput(bs.InputType.PUNCH_RELEASE, self.spaz.on_punch_release)
        
    def _tick(self):
        if len(self.players) != 1:
            return
        if self.spaz2.is_alive():
            self.spaz2.node.handlemessage('knockout', 1000)
        else:
            self.get()
            
    def get(self):
        if self._killed_it:
            return
        self._killed_it = True
        pos = self.spaz2.node.position
        self._kill_sound.play(position=pos)
        self.spaz2.node.delete()
        def do_it():
            babase.app.classic.startup.gameconfig['egg'] = None
            babase.app.config.apply_and_commit()
            
            self._acquire_sound.play(
                position=pos,
            )
            bs.timer(2, bs.app.classic.return_to_main_menu_session_gracefully)
        bs.timer(2, do_it)

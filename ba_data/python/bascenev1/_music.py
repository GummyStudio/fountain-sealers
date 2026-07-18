# Released under the MIT License. See LICENSE for details.
#
"""Music related bits."""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

import _bascenev1

if TYPE_CHECKING:
    pass


class MusicType(Enum):
    """Types of music available to play in-game.

    These do not correspond to specific pieces of music, but rather to
    'situations'. The actual music played for each type can be overridden
    by the game or by the user.
    """

    MENU = 'Menu'
    MENU2 = 'Menu2'
    VICTORY = 'Victory'
    CHAR_SELECT = 'CharSelect'
 
    SCORES = 'Scores'
    RUDE_BUSTER = 'ToTheDeath'
    RUDER_BUSTER = 'rude buster if it was'
    CH4_BUSTER = 'idk the boss'
    RAKUICHI_BUSTER ='im not saying that again'
    MEW_MEW_KISSY = 'pink'
    JEVIL_BOSS = 'metamorphosis'
    KING_BOSS = 'mr hampter'
    DEATH_BY_GLAMOUR = 'gay robot'
    FLOWER_MAN = 'dude he can solo the knight'
    CH4_MENU = 'QUIET_CHURCH'
    SHOP = 'LANTERN'
    TITAN = 'holy shit we are SO DEAD'

def setmusic(musictype: MusicType | None, continuous: bool = False) -> None:
    """Set the app to play (or stop playing) a certain type of music.

    This function will handle loading and playing sound assets as
    necessary, and also supports custom user soundtracks on specific
    platforms so the user can override particular game music with their
    own.

    Pass ``None`` to stop music.

    if ``continuous`` is True and musictype is the same as what is
    already playing, the playing track will not be restarted.
    """

    # All we do here now is set a few music attrs on the current globals
    # node. The foreground globals' current playing music then gets fed to
    # the do_play_music call in our music controller. This way we can
    # seamlessly support custom soundtracks in replays/etc since we're being
    # driven purely by node data.
    gnode = _bascenev1.getactivity().globalsnode
    gnode.music_continuous = continuous
    gnode.music = '' if musictype is None else musictype.value
    gnode.music_count += 1

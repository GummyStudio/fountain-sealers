# Released under the MIT License. See LICENSE for details.
#
"""Provides help related ui."""

from __future__ import annotations

from typing import override

import bauiv1 as bui
import bascenev1lib.actor.spazappearance as spazapp
import random

class AvatarViewWindow(bui.Window):
    """Shows a character's avatar."""
    def __init__(self, character):
        self._width = 800
        self._height = 800
        scale = 0.7
        super().__init__(
            root_widget=bui.containerwidget(
                size=(self._width, self._height),
                toolbar_visibility='menu_minimal',
                scale=scale,
                transition='in_scale',
            ),
        )
        image_sizeoff = 60
        img_w = self._width - image_sizeoff
        img_h = self._height - image_sizeoff
        spaz = character
        bui.imagewidget(
            parent=self._root_widget,
            position=(
                (self._width - img_w) * 0.5,
                (self._height - img_h) * 0.5,
            ),
            size=(img_w, img_h),
            texture=bui.gettexture(spaz.icon_texture),
            tint_texture=bui.gettexture(spaz.icon_mask_texture),
            tint_color=spaz.default_color,
            tint2_color=spaz.default_highlight,
        )
        btn = bui.buttonwidget(
            parent=self._root_widget,
            position=(-10, self._height - 40),
            size=(60, 55),
            scale=1.4,
            label=bui.charstr(bui.SpecialChar.BACK),
            button_type='backSmall',
            extra_touch_border_scale=2.0,
            autoselect=True,
            on_activate_call=self.close,
        )
        
        bui.containerwidget(edit=self._root_widget, cancel_button=btn)
    
    def close(self):
        bui.containerwidget(
            edit=self._root_widget,
            transition='out_scale',
        )

class InventoryWindow(bui.MainWindow):
    """Shows what you got."""

    def __init__(
        self,
        transition: str | None = 'in_right',
        origin_widget: bui.Widget | None = None,
    ):

        bui.set_analytics_screen('Help Window')

        assert bui.app.classic is not None
        uiscale = bui.app.ui_v1.uiscale
        self._width = 1400 if uiscale is bui.UIScale.SMALL else 450
        self._height = (
            1200
            if uiscale is bui.UIScale.SMALL
            else 500
        )
        # xoffs = 70 if uiscale is bui.UIScale.SMALL else 0
        # yoffs = -45 if uiscale is bui.UIScale.SMALL else 0

        # Do some fancy math to fill all available screen area up to the
        # size of our backing container. This lets us fit to the exact
        # screen shape at small ui scale.
        screensize = bui.get_virtual_screen_size()
        scale = (
            1.55
            if uiscale is bui.UIScale.SMALL
            else 1.15 if uiscale is bui.UIScale.MEDIUM else 1.0
        )

        # Calc screen size in our local container space and clamp to a
        # bit smaller than our container size.
        # target_width = min(self._width - 60, screensize[0] / scale)
        target_height = min(self._height - 100, screensize[1] / scale)

        # To get top/left coords, go to the center of our window and
        # offset by half the width/height of our target area.
        yoffs = 0.5 * self._height + 0.5 * target_height + 30.0

        super().__init__(
            root_widget=bui.containerwidget(
                size=(self._width, self._height),
                toolbar_visibility=(
                    'menu_minimal' if uiscale is bui.UIScale.SMALL else 'menu_minimal'
                ),
                scale=scale,
            ),
            transition=transition,
            origin_widget=origin_widget,
            # We're affected by screen size only at small ui-scale.
            refresh_on_screen_size_changes=uiscale is bui.UIScale.SMALL,
        )

        bui.textwidget(
            parent=self._root_widget,
            position=(
                self._width * 0.5,
                yoffs - (50 if uiscale is bui.UIScale.SMALL else 30),
            ),
            size=(0, 0),
            text=bui.Lstr(resource='inventoryText'),
            color=bui.app.ui_v1.title_color,
            scale=0.9 if uiscale is bui.UIScale.SMALL else 1.0,
            maxwidth=(130 if uiscale is bui.UIScale.SMALL else 200),
            h_align='center',
            v_align='center',
        )

        if uiscale is bui.UIScale.SMALL:
            bui.containerwidget(
                edit=self._root_widget, on_cancel_call=self.main_window_back
            )
        else:
            btn = bui.buttonwidget(
                parent=self._root_widget,
                position=(50, yoffs - 50),
                size=(60, 55),
                scale=0.8,
                label=bui.charstr(bui.SpecialChar.BACK),
                button_type='backSmall',
                extra_touch_border_scale=2.0,
                autoselect=True,
                on_activate_call=self.main_window_back,
            )
            bui.containerwidget(edit=self._root_widget, cancel_button=btn)

        button_width = 300
        yoffs -= 120
        self._player_profiles_button = btn = bui.buttonwidget(
            parent=self._root_widget,
            position=(self._width * 0.5 - button_width * 0.5, yoffs),
            autoselect=True,
            size=(button_width, 60),
            label=bui.Lstr(resource='playerProfilesWindow.titleText'),
            color=(0.55, 0.5, 0.6),
            icon=bui.gettexture('cuteSpaz'),
            textcolor=(0.75, 0.7, 0.8),
            on_activate_call=self._player_profiles_press,
        )
        yoffs -= 20
        bui.textwidget(
            parent=self._root_widget,
            position=(
                self._width * 0.5,
                yoffs,
            ),
            size=(0, 0),
            text=bui.Lstr(resource='yourCharactersText'),
            color=(0.8, 0.9, 1, 0.6),
            scale=0.8,
            maxwidth=self._width - 300,
            h_align='center',
            v_align='center',
        )
        if uiscale is bui.UIScale.SMALL:
            scroll_width = self._width * 0.5
        else:
            scroll_width = self._width - 140
        scroll_height = 300
        yoffs -= 10 + scroll_height
        apps = spazapp.get_appearances()
        app_btn_height = 80
        app_btn_width = scroll_width - 15
        sub_height = (app_btn_height + 8) * len(apps)
        sub_width = scroll_width
        app_btn_y = sub_height - app_btn_height
        app_btn_xoffs = -3
        self._scrollwidget = bui.scrollwidget(
            parent=self._root_widget,
            size=(scroll_width, scroll_height),
            position=(self._width * 0.5 - scroll_width * 0.5, yoffs),
            simple_culling_v=100.0,
            capture_arrows=True,
            border_opacity=0.4,
            center_small_content_horizontally=True,
        )
        self._subcontainer = bui.containerwidget(
            parent=self._scrollwidget,
            size=(sub_width, sub_height),
            background=False,
            claims_left_right=False,
        )
        for spaz in apps:
            first = False
            if apps.index(spaz) == 0:
                first = True
            spaz = bui.app.classic.spaz_appearances[spaz]
            name = bui.Lstr(translate=('characterNames', spaz.name))
            btn = bui.buttonwidget(
                parent=self._subcontainer,
                position=(sub_width * 0.5 - app_btn_width * 0.5 + app_btn_xoffs, app_btn_y),
                size=(app_btn_width, app_btn_height),
                label='',
                color=(0.55, 0.5, 0.6),
                textcolor=(0.75, 0.7, 0.8),
                on_activate_call=bui.WeakCall(self._play_random_voiceline, spaz),
                enable_sound=False,
            )
            bui.textwidget(
                parent=self._subcontainer,
                position=(
                    sub_width * 0.5 - app_btn_width * 0.5 + app_btn_xoffs + (app_btn_height), 
                    app_btn_y + (app_btn_height * 0.5) + 20,
                ),
                size=(0, 0),
                text=name,
                draw_controller=btn,
                scale=0.9,
                maxwidth=app_btn_width - 120,
                h_align='left',
            )
            bui.buttonwidget(
                parent=self._subcontainer,
                position=(
                    sub_width * 0.5 - app_btn_width * 0.5 + app_btn_xoffs + 10, 
                    app_btn_y + (27 * 0.5)
                ),
                size=(app_btn_height - 27, app_btn_height - 27),
                label='',
                color=(1, 1, 1),
                texture=bui.gettexture(spaz.icon_texture),
                tint_texture=bui.gettexture(spaz.icon_mask_texture),
                tint_color=spaz.default_color,
                tint2_color=spaz.default_highlight,
                mask_texture=bui.gettexture('characterIconMask'),
                on_activate_call=bui.WeakCall(self._show_avatar, spaz),
                selectable=False,
            )
            if first:
                bui.buttonwidget(
                    edit=btn,
                    up_widget=self._player_profiles_button,
                )
            app_btn_y -= app_btn_height + 5
        
    def _show_avatar(self, spaz):
        # no-op if our underlying widget is dead or on its way out.
        if not self._root_widget or self._root_widget.transitioning_out:
            return
        AvatarViewWindow(spaz)
    
    def _play_random_voiceline(self, spaz):
        voicelines = [
            spaz.jump_sounds,
            spaz.attack_sounds,
            spaz.impact_sounds,
            spaz.death_sounds,
            spaz.pickup_sounds,
            spaz.fall_sounds,
        ]
        chosen = random.choice(voicelines)
        bui.getsound(random.choice(chosen)).play()

    def _player_profiles_press(self) -> None:
        # pylint: disable=cyclic-import
        from bauiv1lib.profile.browser import ProfileBrowserWindow

        # no-op if our underlying widget is dead or on its way out.
        if not self._root_widget or self._root_widget.transitioning_out:
            return

        self.main_window_replace(
            ProfileBrowserWindow(origin_widget=self._player_profiles_button)
        )

    @override
    def get_main_window_state(self) -> bui.MainWindowState:
        # Support recreating our window for back/refresh purposes.
        cls = type(self)
        return bui.BasicMainWindowState(
            create_call=lambda transition, origin_widget: cls(
                transition=transition, origin_widget=origin_widget
            )
        )

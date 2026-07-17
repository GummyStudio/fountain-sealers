# Released under the MIT License. See LICENSE for details.
#
"""Provides a picker for characters."""

from __future__ import annotations

import math
from typing import TYPE_CHECKING, override

from bauiv1lib.popup import PopupWindow
import bauiv1 as bui

if TYPE_CHECKING:
    from typing import Any, Sequence


class CharacterPickerDelegate:
    """Delegate for character-picker."""

    def on_character_picker_pick(self, character: str) -> None:
        """Called when a character is selected."""
        raise NotImplementedError()

    def on_character_picker_get_more_press(self) -> None:
        """Called when the 'get more characters' button is pressed."""
        raise NotImplementedError()


class TagPickerPopup(PopupWindow):
    def __init__(self, picker: CharacterPicker, position: tuple[float, float], tags: list[Any]):
        self._picker = picker
        self._transitioning_out = False
        self._tags = tags
        self._r = 'delta.tagFilter'
        
        width = 220
        height = 60 + max(1, len(tags)) * 35
        
        super().__init__(
            position=position,
            size=(width, height),
            scale=1.2,
            bg_color=(0.3, 0.3, 0.3),
        )
        
        bui.textwidget(
            parent=self.root_widget,
            position=(10, height - 35),
            size=(width - 20, 25),
            text=bui.Lstr(
                resource=self._r+'.titleText'
            ),
            scale=0.8,
            h_align="center",
            v_align="center",
            color=(0.8, 0.8, 0.8),
        )
        
      

        for i, tag in enumerate(tags):
            tag_name = bui.Lstr(resource=self._r+'.tags.'+str(tag.value))
            is_active = tag in self._picker._active_tags
            
            bui.checkboxwidget(
                parent=self.root_widget,
                position=(20, height - 70 - i * 35),
                size=(width - 40, 30),
                text=tag_name,
                value=is_active,
                maxwidth=width - 60,
                scale=0.8,
                on_value_change_call=bui.Call(self._toggle_tag, tag),
            )
            
    def _toggle_tag(self, tag: Any, value: bool) -> None:
        if value:
            self._picker._active_tags.add(tag)
        else:
            self._picker._active_tags.discard(tag)
        self._picker._refresh_characters()

    @override
    def on_popup_cancel(self) -> None:
        bui.getsound('swish').play()
        self._transition_out()
    
    def _transition_out(self) -> None:
        if not self._transitioning_out:
            self._transitioning_out = True
            bui.containerwidget(edit=self.root_widget, transition='out_scale')

class CharacterPicker(PopupWindow):
    """Popup window for selecting characters."""

    def __init__(
        self,
        parent: bui.Widget,
        position: tuple[float, float] = (0.0, 0.0),
        delegate: CharacterPickerDelegate | None = None,
        scale: float | None = None,
        offset: tuple[float, float] = (0.0, 0.0),
        tint_color: Sequence[float] = (1.0, 1.0, 1.0),
        tint2_color: Sequence[float] = (1.0, 1.0, 1.0),
        selected_character: str | None = None,
    ):
        # pylint: disable=too-many-locals
        # pylint: disable=too-many-positional-arguments
        from bascenev1lib.actor import spazappearance

        assert bui.app.classic is not None

        del parent  # unused here
        uiscale = bui.app.ui_v1.uiscale
        if scale is None:
            scale = (
                1.85
                if uiscale is bui.UIScale.SMALL
                else 1.65 if uiscale is bui.UIScale.MEDIUM else 1.23
            )

        self._delegate = delegate
        self._transitioning_out = False

        self._spazzes = spazappearance.get_appearances()
        self._spazzes.sort()
        self._icon_textures = [
            bui.gettexture(bui.app.classic.spaz_appearances[s].icon_texture)
            for s in self._spazzes
        ]
        self._icon_tint_textures = [
            bui.gettexture(
                bui.app.classic.spaz_appearances[s].icon_mask_texture
            )
            for s in self._spazzes
        ]

        count = len(self._spazzes)

        columns = 3
        rows = int(math.ceil(float(count) / columns))

        button_width = 100
        button_height = 100
        button_buffer_h = 10
        button_buffer_v = 15

        self._width = 10 + columns * (button_width + 2 * button_buffer_h) * (
            1.0 / 0.95
        ) * (1.0 / 0.8)
        self._height = self._width * (
            0.8 if uiscale is bui.UIScale.SMALL else 1.06
        )

        self._scroll_width = self._width * 0.8
        self._scroll_height = self._height * 0.8
        self._scroll_position = (
            (self._width - self._scroll_width) * 0.5,
            (self._height - self._scroll_height) * 0.5,
        )

        self.last_filter_txt = 'kjFdjknjfksnjd'
        self._last_active_tags_hash = None
        
        # Creates our _root_widget.
        super().__init__(
            position=position,
            size=(self._width, self._height),
            scale=scale,
            bg_color=(0.5, 0.5, 0.5),
            offset=offset,
            focus_position=self._scroll_position,
            focus_size=(self._scroll_width, self._scroll_height),
        )

        self._scrollwidget = bui.scrollwidget(
            parent=self.root_widget,
            size=(self._scroll_width, self._scroll_height),
            color=(0.55, 0.55, 0.55),
            highlight=False,
            position=self._scroll_position,
        )
        bui.containerwidget(edit=self._scrollwidget, claims_left_right=True)

        self._sub_width = self._scroll_width * 0.95
        self._sub_height = (
            5 + rows * (button_height + 2 * button_buffer_v) + 100
        )
        self._subcontainer = bui.containerwidget(
            parent=self._scrollwidget,
            size=(self._sub_width, self._sub_height),
            background=False,
        )
        
        # Shrunk textwidget slightly to fit the Tags button next to it
        self._filter_text = bui.textwidget(
            parent=self.root_widget,
            position=(20, self._height - 45),
            size=(self._width - 160, 35),
            editable=True,
            text='',
            max_chars=32,
            on_return_press_call=bui.Call(self._refresh_characters),
        )
        
        self._tags_button = bui.buttonwidget(
            parent=self.root_widget,
            position=(self._width - 130, self._height - 45),
            size=(110, 35),
            label=bui.Lstr(resource='delta.tagFilter.titleText'),
            scale=0.8,
            autoselect=True,
            on_activate_call=bui.Call(self._open_tags_popup),
        )
        
        self._columns = 3
        self._button_width = 100
        self._button_height = 100
        self._button_buffer_h = 10
        self._button_buffer_v = 15

        self._tint_color = tint_color
        self._tint2_color = tint2_color
        self._selected_character = selected_character

        self._character_widgets = []
        self._get_more_characters_button = btn = bui.buttonwidget(
            parent=self._subcontainer,
            size=(self._sub_width * 0.8, 60),
            position=(self._sub_width * 0.1, 30),
            label=bui.Lstr(resource='editProfileWindow.getMoreCharactersText'),
            on_activate_call=self._on_store_press,
            color=(0.6, 0.6, 0.6),
            textcolor=(0.8, 0.8, 0.8),
            autoselect=True,
        )
        bui.widget(edit=btn, show_buffer_top=30, show_buffer_bottom=30)
        self._active_tags = set()
        
        self._refresh_characters()
       
        self.tick_timer = bui.AppTimer(0.1, self._refresh_characters)
    
    def _open_tags_popup(self) -> None:
        tags = set()
        for s in self._spazzes:
            try:
                c_tags = getattr(bui.app.classic.spaz_appearances[s], 'tags', [])
                for t in c_tags:
                    tags.add(t)
            except Exception:
                pass
        
        TagPickerPopup(
            picker=self,
            position=(20, 50),
            tags=tags
        )
        
    def _refresh_characters(self) -> None:
        if self._transitioning_out:
            self.tick_timer = None
            return
        else:
            self.tick_timer = bui.AppTimer(0.1, self._refresh_characters)
        
        search = ""
        if self._filter_text is not None:
            search = (
                bui.textwidget(query=self._filter_text)
                .lower()
                .strip()
            )

        active_tags_hash = hash(frozenset(self._active_tags))
        if search == self.last_filter_txt and active_tags_hash == self._last_active_tags_hash:
            # Nothing changed
            return
        self.last_filter_txt = search
        self._last_active_tags_hash = active_tags_hash
        
        for widget in self._character_widgets:
            try:
                widget.delete()
            except Exception:
                pass
        self._character_widgets.clear()

        # Get an evaluated lstr to make it feel better
        translations = {}
        for spaz in self._spazzes:
            if spaz == "Vessel":
                try:
                    name = (
                        bui.app.classic.startup.gameconfig[
                            "SurveyChoices"
                        ]["vessel_name"]
                        .strip()
                        .lower()
                        .capitalize()
                    )
                except Exception:
                    name = bui.Lstr(
                        translate=("characterNames", spaz)
                    ).evaluate()
            else:
                name = bui.Lstr(
                    translate=("characterNames", spaz)
                ).evaluate()
            if name:
                translations[spaz] = name

        # Filter characters by both search phrase and active tag configurations
        characters = []
        for c in self._spazzes:
            if search not in translations.get(c, "").lower().strip():
                continue
                
            if self._active_tags:
                try:
                    c_tags = set(getattr(bui.app.classic.spaz_appearances[c], 'tags', []))
                    if not self._active_tags.issubset(c_tags):
                        continue
                except Exception:
                    continue
            characters.append(c)

        columns = self._columns
        rows = max(1, math.ceil(len(characters) / columns))
        self._sub_height = (
            5
            + rows * (self._button_height + 2 * self._button_buffer_v)
            + 100
        )

        bui.containerwidget(
            edit=self._subcontainer,
            size=(self._sub_width, self._sub_height),
        )

        mask_texture = bui.gettexture("characterIconMask")

        for index, character in enumerate(characters):
            row = index // columns
            col = index % columns

            pos = (
                col * (self._button_width + 2 * self._button_buffer_h)
                + self._button_buffer_h,

                self._sub_height
                - (row + 1)
                * (self._button_height + 2 * self._button_buffer_v)
                + 12,
            )
            try:
                texture = bui.gettexture(
                    bui.app.classic.spaz_appearances[
                        character
                    ].icon_texture
                )

                tint_texture = bui.gettexture(
                    bui.app.classic.spaz_appearances[
                        character
                    ].icon_mask_texture
                )
            except Exception:
                continue
                
            btn = bui.buttonwidget(
                parent=self._subcontainer,
                button_type="square",
                size=(self._button_width, self._button_height),
                position=pos,
                texture=texture,
                tint_texture=tint_texture,
                mask_texture=mask_texture,
                label="",
                color=(1, 1, 1),
                tint_color=self._tint_color,
                tint2_color=self._tint2_color,
                autoselect=True,
                on_activate_call=bui.Call(
                    self._select_character,
                    character,
                ),
            )

            if character == self._selected_character:
                bui.containerwidget(
                    edit=self._subcontainer,
                    selected_child=btn,
                    visible_child=btn,
                )

            if character == "Vessel":
                try:
                    name = (
                        bui.app.classic.startup.gameconfig[
                            "SurveyChoices"
                        ]["vessel_name"]
                        .strip()
                        .capitalize()
                    )
                except Exception:
                    name = bui.Lstr(
                        translate=("characterNames", character)
                    )
            else:
                name = bui.Lstr(
                    translate=("characterNames", character)
                )

            label = bui.textwidget(
                parent=self._subcontainer,
                text=name,
                position=(
                    pos[0] + self._button_width * 0.5,
                    pos[1] - 12,
                ),
                size=(0, 0),
                scale=0.5,
                maxwidth=self._button_width,
                draw_controller=btn,
                h_align="center",
                v_align="center",
                color=(0.8, 0.8, 0.8, 0.8),
            )

            self._character_widgets.extend((btn, label))

    def _on_store_press(self) -> None:
        from bauiv1lib.account.signin import show_sign_in_prompt

        plus = bui.app.plus
        assert plus is not None

        if plus.get_v1_account_state() != 'signed_in':
            show_sign_in_prompt()
            return

        if self._delegate is not None:
            self._delegate.on_character_picker_get_more_press()

        self._transition_out()

    def _select_character(self, character: str) -> None:
        if self._delegate is not None:
            self._delegate.on_character_picker_pick(character)
        self._transition_out()

    def _transition_out(self) -> None:
        if not self._transitioning_out:
            self._transitioning_out = True
            bui.containerwidget(edit=self.root_widget, transition='out_scale')

    @override
    def on_popup_cancel(self) -> None:
        bui.getsound('swish').play()
        self._transition_out()
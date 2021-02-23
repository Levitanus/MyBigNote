import typing as ty

import pygame
import pygame.locals as lc
import pygame_gui

from .midi_in import SingleNoteInput
MIDI_HEIGHT = 30


class MidiPrefsWidget:

    def __init__(
        self,
        screen: pygame.surface.Surface,
        manager: pygame_gui.UIManager,
        rect: pygame.Rect,
        bg: ty.Tuple[int, int, int] = (150, 150, 150),
    ) -> None:
        self.screen = screen
        self.manager = manager
        self.rect = rect
        self.midi_in = SingleNoteInput()
        self.midi_in.init()
        self.bg = bg

        dropdown_rect = (0, 0, 200, MIDI_HEIGHT)

        rect = pygame.Rect(*dropdown_rect)
        rect.topleft = (self.rect.x, self.rect.y)
        keys = list(self.midi_in.apis.keys())
        self.api = pygame_gui.elements.UIDropDownMenu(
            keys, keys[0], rect, self.manager
        )

        rect = pygame.Rect(*dropdown_rect)
        rect.topright = (self.rect.x + self.rect.width, self.rect.y)
        keys = list(self.midi_in.ports)
        self.port = pygame_gui.elements.UIDropDownMenu(
            keys, keys[0], rect, self.manager
        )

    @property
    def note(self) -> ty.Optional[int]:
        return self.midi_in.note

    def update(self, event: pygame.event.Event) -> None:
        if event.type != pygame.USEREVENT:
            return
        if event.user_type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
            if event.ui_element is self.api:
                self.midi_in.init(self.midi_in.apis[event.text])
                self.port.options_list.clear()
                self.port.options_list.extend(self.midi_in.ports)
                self.port.selected_option = self.port.options_list[0]
            if event.ui_element is self.port:
                self.midi_in.use_port(self.midi_in.ports.index(event.text))

    def draw(self) -> None:
        """draw"""

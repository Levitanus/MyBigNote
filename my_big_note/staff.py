import typing as ty

import pygame
# import pygame.locals as lc
import pygame_gui
from pathlib import Path

from .gui_tools import load_svg
from .midi_prefs import MIDI_HEIGHT

_note_lines = {
    0: ((0, ''), ),  # C
    1: ((0, 'sharp'), (0.5, 'flat')),  # C#
    2: ((.5, ''), ),  # D
    3: ((.5, 'sharp'), (1, 'flat')),  # D#
    4: ((1, ''), ),  # E
    5: ((1.5, ''), ),  # F
    6: ((1.5, 'sharp'), (2, 'flat')),  # F#
    7: ((2, ''), ),  #G
    8: ((2, 'sharp'), (2.5, 'flat')),  # G#
    9: ((2.5, ''), ),  # A
    10: ((2.5, 'sharp'), (3, 'flat')),  # A#
    11: ((3, ''), ),  # B
    12: ((3.5, ''), ),  # C
    13: ((3.5, 'sharp'), (4, 'flat')),  # C#
    14: ((4, ''), ),  # D
    15: ((4, 'sharp'), (4.5, 'flat')),  # D#
    16: ((4.5, ''), ),  # E
    17: ((5, ''), ),  # F
    18: ((5, 'sharp'), (5.5, 'flat')),  # F#
    19: ((5.5, ''), ),  # G
    20: ((5.5, 'sharp'), (6, 'flat')),  # G#
    21: ((6, ''), ),  # A
    22: ((6, 'sharp'), (6.5, 'flat')),  # A#
    23: ((6.5, ''), ),  # B
}


def get_note(note: int, want_flat: bool = False) -> ty.Tuple[float, str]:
    index = 1 if want_flat else 0
    line_ofst, alteration = _note_lines[note % 24][index]
    line_7 = (note // 24) * 7
    return line_7 + line_ofst, alteration


class Staff:

    def __init__(
        self, screen: pygame.surface.Surface, rect: pygame.Rect,
        manager: pygame_gui.UIManager
    ) -> None:
        self.screen = screen
        self.manager = manager
        self.rect = rect
        # self.rect.height -= MIDI_HEIGHT
        # self.rect.topleft = self.rect.x, self.rect.y + MIDI_HEIGHT
        self.max_lines = 9

        dropdown_rect = (0, 0, 200, MIDI_HEIGHT)
        rect = pygame.Rect(*dropdown_rect)
        rect.bottomleft = (0, self.screen.get_height())
        keys = ['auto', 'скрипичный', 'басовый']
        self.clef = pygame_gui.elements.UIDropDownMenu(
            keys,
            keys[0],
            rect,
            self.manager,
        )
        self.clef.expand_direction = 'up'
        for state in self.clef.menu_states.values():
            state.expand_direction = 'up'
        self.selected_clef = keys[0]
        self._bottomline_note: int
        self._note: ty.Optional[int] = None
        # self.note = 58

    @property
    def selected_clef(self) -> str:
        return self._selected_clef

    @selected_clef.setter
    def selected_clef(self, clef: str) -> None:
        if clef == 'скрипичный':
            self._selected_clef = clef
            self._bottomline_note = ty.cast(int, get_note(64)[0])
            return
        if clef == 'басовый':
            self._selected_clef = clef
            self._bottomline_note = ty.cast(int, get_note(43)[0])
            return
        if clef == 'auto':
            self.selected_clef = 'скрипичный'
            return
        raise ValueError(f'can not set clef to {clef}')

    @property
    def note(self) -> ty.Optional[int]:
        return self._note

    @note.setter
    def note(self, note: ty.Optional[int]) -> None:
        self._note = note
        if note is None:
            return
        if self.clef.selected_option == 'auto':
            if note < 57:
                self.selected_clef = 'басовый'
            else:
                self.selected_clef = 'скрипичный'

    @property
    def line_w(self) -> int:
        w = self.rect.height // 100
        if w < 3:
            w = 3
        return w

    @property
    def line_h(self) -> float:
        return self.rect.height / self.max_lines

    @property
    def lines_rect(self) -> pygame.Rect:
        v_offset = self.line_h * ((self.max_lines - 5) / 2)
        margins = (0, v_offset, 0, v_offset)
        rect = pygame.Rect(
            self.rect.x + margins[0], self.rect.y + margins[1],
            self.rect.width - (margins[2] * 2),
            self.rect.height - (margins[3] * 2)
        )
        return rect

    def draw_line(
        self,
        line_nr: int,
        width: ty.Optional[int] = None,
        center: ty.Optional[ty.Tuple[int, int]] = None
    ) -> None:
        l_rect = self.lines_rect
        bottom = l_rect.bottom
        if width is not None:
            if center is None:
                center = l_rect.center
            l_rect.width = width
            l_rect.center = center
        pos_y = bottom - self.line_h * (line_nr - 1)
        pygame.draw.line(
            self.screen,
            (0, 0, 0),
            (
                l_rect.x,
                pos_y,
            ),
            (
                l_rect.right,
                pos_y,
            ),
            width=self.line_w,
        )

    def draw_clef(self) -> pygame.Rect:
        clef = self.selected_clef
        lines_rect = self.lines_rect
        current_path = Path(__file__).absolute().parent
        if clef == 'скрипичный':
            path = current_path / Path('images/treble clef.svg')
            png = load_svg(str(path), int(self.line_h * 6))
            new_y = 0 - int(self.line_h)
        elif clef == 'басовый':
            path = current_path / Path('images/bass clef.svg')
            png = load_svg(str(path), int(self.line_h * 4))
            new_y = 0
        rect = png.get_rect()
        rect.bottomleft = lines_rect.bottomleft
        rect.x += int(self.rect.width / 100 * 5)
        rect.y -= new_y
        self.screen.blit(png, rect)
        return ty.cast(pygame.Rect, rect)

    def draw_note(self, clef_rect: pygame.Rect) -> None:
        if self.note is None:
            return
        note_line, alteration = get_note(self.note)

        line_nr = note_line - self._bottomline_note
        lines_rect = self.lines_rect
        lines_rect.x += clef_rect.width
        lines_rect.width -= clef_rect.width
        current_path = Path(__file__).absolute().parent
        path = current_path / Path('images/note.svg')
        notepng = load_svg(str(path), int(self.line_h))
        new_y = lines_rect.bottom - self.line_h * (line_nr)

        rect = notepng.get_rect()
        rect.center = lines_rect.center[0], int(new_y)
        self.screen.blit(notepng, rect)

        if alteration:
            path = current_path / Path(f'images/{alteration}.svg')
            altpng = load_svg(str(path), int(self.line_h * 1.5))
            alt_rect = altpng.get_rect()
            alt_rect.center = rect.center
            alt_rect.x -= rect.width
            self.screen.blit(altpng, alt_rect)
        if line_nr >= 5.0 or line_nr <= -1.0:
            intline = int(line_nr)
            r_v = (6, intline + 2) if intline >= 5 else (0, intline, -1)
            for line in range(*r_v):
                self.draw_line(
                    line,
                    width=rect.width + rect.width // 2,
                    center=rect.center
                )

    def update(self, event: pygame.event.Event) -> None:
        if event.type != pygame.USEREVENT:
            return
        if event.user_type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
            if event.ui_element is self.clef:
                self.selected_clef = event.text

    def draw(self) -> None:
        # for line in range(-1, 6):
        for line in range(5):
            self.draw_line(line + 1)
        if self.clef.selected_option == self.selected_clef == 'auto':
            self.selected_clef = 'скрипичный'
        clef_rect = self.draw_clef()
        self.draw_note(clef_rect)

    def resize(self) -> None:
        """"""
        self.clef.rect.bottomleft = 0, self.screen.get_height()
        self.clef.set_relative_position((self.clef.rect.x, self.clef.rect.y))

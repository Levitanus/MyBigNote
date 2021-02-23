import typing as ty
from pathlib import Path

import pygame
import pygame.locals as lc
import pygame_gui

from .midi_prefs import MidiPrefsWidget, MIDI_HEIGHT
from .staff import Staff
from .gui_tools import load_svg


class App:
    """Create a single-window app with multiple scenes."""

    def __init__(self) -> None:
        """Initialize pygame and the application."""
        pygame.init()
        self.flags = lc.RESIZABLE
        size = (500, 500)
        self.screen = pygame.display.set_mode(size, self.flags)
        self.running = True
        pygame.display.set_caption('MyBigNote (by Levitanus)')
        pygame.display.set_icon(
            load_svg(str(Path(__file__).parent / Path('images/note.svg')), 25)
        )
        self.manager = pygame_gui.UIManager(size)

        self.staff = Staff(
            self.screen, self.staff_rect(MIDI_HEIGHT), self.manager
        )
        self.midi = MidiPrefsWidget(
            self.screen, self.manager, self.midi_rect(MIDI_HEIGHT)
        )

    def midi_rect(self, midi_height: int) -> pygame.Rect:
        return pygame.Rect(0, 0, self.screen.get_width(), midi_height)

    def staff_rect(self, midi_height: int) -> pygame.Rect:
        x, y, width, height = (
            0, midi_height, self.screen.get_width(),
            self.screen.get_height() - midi_height
        )
        h_margins = int(width / 100 * 5)
        v_margins = int(height / 100 * 10)
        rect = pygame.Rect(
            x + h_margins, y + v_margins, width - h_margins * 2,
            height - v_margins * 2
        )
        return rect

    def run(self) -> None:
        """Run the main event loop."""
        clock = pygame.time.Clock()
        while self.running:
            time_delta = clock.tick(20) / 1000.0
            events = pygame.event.get()
            for event in events:
                if event.type == lc.QUIT:
                    self.running = False
                elif event.type == pygame.VIDEORESIZE:
                    self.resize()
                    # pygame.display.update()
                elif event.type == pygame.VIDEOEXPOSE:
                    self.resize()
                    # pygame.display.update()
                self.midi.update(event)
                self.staff.update(event)
                self.manager.process_events(event)
            self.manager.update(time_delta)

            self.draw()
            self.manager.draw_ui(self.screen)

            pygame.display.update()
        pygame.quit()

    def resize(self) -> None:
        rect = self.manager.get_root_container().get_rect()
        rect.width, rect.height = self.screen.get_width(
        ), self.screen.get_height()
        self.midi.rect = self.midi_rect(MIDI_HEIGHT)
        self.staff.rect = self.staff_rect(MIDI_HEIGHT)
        self.staff.resize()
        # self.draw()

    def draw(self) -> None:
        self.screen.fill((255, 255, 255))
        self.staff.note = self.midi.note
        self.midi.draw()
        self.staff.draw()


if __name__ == '__main__':
    App().run()

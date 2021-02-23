import cairosvg
import io
import pygame


def load_svg(filename: str, height: int = 512) -> pygame.surface.Surface:
    new_bites = cairosvg.svg2png(url=filename, output_height=height)
    byte_io = io.BytesIO(new_bites)
    return pygame.image.load(byte_io)
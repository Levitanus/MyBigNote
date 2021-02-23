from my_big_note.staff import get_note
from pprint import pprint

notes = {
    'C3': 60,
    'C#3': 61,
    'D3': 62,
    'D#3': 63,
    'E3': 64,
    'C4': 72,
    'C#4': 73,
    'C-2': 0,
    'C#-2': 1,
    'D-2': 2,
    'D#-2': 3,
    'E-2': 4,
    'C0': 0 + 24,
    'C#0': 1 + 24,
    'D0': 2 + 24,
    'D#0': 3 + 24,
    'E0': 4 + 24,
}

pprint(
    list(
        f'{note_key}: {get_note(note_value)}'
        for note_key, note_value in notes.items()
    )
)

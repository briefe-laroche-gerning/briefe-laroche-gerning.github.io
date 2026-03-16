# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Hilfsfunktionen, die in mehreren Tests zur semantischen Erschließung gebraucht werden #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

from os.path import basename
import re
from operator import itemgetter


def fix_hyphenation(text):
    """
    Führt Silbentrennungen am Ende einer Zeile zusammen, wenn das Wort durch - oder = verbunden ist.
    """
    text = re.sub(
        r'(\w+)(?:[-=]\s*\r?\n\s*[-=]|[-=]\s*\r?\n\s*|\s*\r?\n\s*[-=])(\w+)',
        r'\1\2',
        text
    )
    return text


def sort_letters(letters):
    """
    Sortiert Brief-Dateien nach ihrer Nummer.
    """

    # Extrahiere Nummer aus dem Namen der Datei: Tupel (Fateiname, Nummer)
    letters_with_num = [
        (f, int(re.search(r'\d+', basename(f)).group()))
        for f in letters
    ]

    # Sortiere nach Nummer
    sorted_letters = [f[0] for f in sorted(letters_with_num, key=itemgetter(1))]

    return sorted_letters
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Hilfsfunktionen, die in mehreren Tests zur semantischen Erschließung gebraucht werden, stehen hier  #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

from os.path import basename
import re
from operator import itemgetter

def fix_hyphenation(text):
    """
    Removes hyphenation at the end of a line (words separated by - or =).
    """
    text = re.sub(
        r'(\w+)(?:[-=]\s*\r?\n\s*[-=]|[-=]\s*\r?\n\s*|\s*\r?\n\s*[-=])(\w+)',
        r'\1\2',
        text
    )
    return text


def sort_letters(letters):
    """
    Sorts letter files by number.
    """

    # Extract number from file name, listtuples (filename, number)
    letters_with_num = [
        (f, int(re.search(r'\d+', basename(f)).group()))
        for f in letters
    ]

    # Sort by number
    sorted_letters = [f[0] for f in sorted(letters_with_num, key=itemgetter(1))]

    return sorted_letters
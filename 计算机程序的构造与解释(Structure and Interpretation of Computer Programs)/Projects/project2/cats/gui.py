"""Web server for the typing GUI."""
import base64
import os
import random
import string

import cats
from gui_files.common_server import Server, route, sendto, start
from gui_files import multiplayer

PORT = 31415
DEFAULT_SERVER = 'https://cats.cs61a.org'
GUI_FOLDER = "gui_files/"
PARAGRAPH_PATH = "./data/sample_paragraphs.txt"
WORDS_LIST = cats.lines_from_file('data/words.txt')
WORDS_SET = set(WORDS_LIST)
LETTER_SETS = [(w, set(w)) for w in WORDS_LIST]
SIMILARITY_LIMIT = 2


@route
def request_paragraph(topics=None):
    """Return a random paragraph."""
    paragraphs = cats.lines_from_file(PARAGRAPH_PATH)
    random.shuffle(paragraphs)
    select = cats.about(topics) if topics else lambda x: True
    return cats.choose(paragraphs, select, 0)


@route
def analyze(prompted_text, typed_text, start_time, end_time):
    """Return [wpm, accuracy]."""
    return {
        "wpm": cats.wpm(typed_text, end_time - start_time),
        "accuracy": cats.accuracy(typed_text, prompted_text)
    }


def similar(w, v, n):
    """Whether W intersect V contains at least |W|-N and |V|-N elements."""
    intersect = len(w.intersection(v))
    return intersect >= len(w) - n and intersect >= len(v) - n


@route
def autocorrect(word=""):
    """Call autocorrect using the best score function available."""
    raw_word = word
    word = cats.lower(cats.remove_punctuation(raw_word))
    if word in WORDS_SET or word == '':
        return raw_word

    # Heuristically choose candidate words to score.
    letters = set(word)
    candidates = [w for w, s in LETTER_SETS if similar(s, letters, SIMILARITY_LIMIT)]

    # Try various diff functions until one doesn't raise an exception.
    for fn in [cats.final_diff, cats.feline_fixes, cats.sphinx_swap]:
        try:
            guess = cats.autocorrect(word, candidates, fn, SIMILARITY_LIMIT)
            return reformat(guess, raw_word)
        except BaseException:
            pass

    return raw_word


def reformat(word, raw_word):
    """Reformat WORD to match the capitalization and punctuation of RAW_WORD."""
    # handle capitalization
    if raw_word != "" and raw_word[0].isupper():
        word = word.capitalize()

    # find the boundaries of the raw word
    first = 0
    while first < len(raw_word) and raw_word[first] in string.punctuation:
        first += 1
    last = len(raw_word) - 1
    while last > first and raw_word[last] in string.punctuation:
        last -= 1

    # add wrapping punctuation to the word
    if raw_word != word:
        word = raw_word[:first] + word
        word = word + raw_word[last + 1:]

    return word


###############
# Multiplayer #
###############

@route
def request_id():
    if not cats.enable_multiplayer:
        return
    return Server.provide_id()


@route
def report_progress(id, typed, prompt):
    """Report progress to the multiplayer server and also return it."""
    typed = typed.split()  # A list of word strings
    prompt = prompt.split()  # A list of word strings

    return cats.report_progress(typed, prompt, id, sendto(Server.set_progress))


@route
def fastest_words(prompt, targets):
    """Return a list of word_speed values describing the game."""
    words = prompt.split()
    progress = Server.request_all_progress(targets=targets)
    start_times = [p[0][1] for p in progress]
    times_per_player = [[p[1] - s for p in ps] for s, ps in zip(start_times, progress)]
    game = cats.time_per_word(times_per_player, words)
    return cats.fastest_words(game)


multiplayer.create_multiplayer_server()

###############
# Favicons #
###############


@route
def favicon():
    favicon_folder = os.path.join(GUI_FOLDER, "favicons")
    favicons = os.listdir(favicon_folder)
    path = os.path.join(favicon_folder, random.choice(favicons))
    with open(path, "rb") as f:
        data = f.read()
    image_b64 = base64.b64encode(data).decode("utf-8")
    return "data:image/png;base64," + image_b64


if __name__ == "__main__" or "gunicorn" in os.environ.get("SERVER_SOFTWARE", ""):
    app = start(PORT, DEFAULT_SERVER, GUI_FOLDER, multiplayer.db_init)
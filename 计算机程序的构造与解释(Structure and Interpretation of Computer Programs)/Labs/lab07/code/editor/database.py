import sqlite3
from random import randrange
from typing import Tuple, Union


def get_word() -> str:
    with open("src/words.txt") as file:
        word = next(file)
        for i, trial in enumerate(file):
            if randrange(i + 2) != 0:
                continue
            word = trial
        return word


def generate_id(n=3):
    return "".join(get_word().lower().capitalize().strip() for _ in range(3))


def save(code_lines, skip_envs, hide_return_frames):
    conn = sqlite3.connect("saved")
    to_store = repr(code_lines)
    lookup = generate_id()
    conn.execute("INSERT INTO stored_lines VALUES(?, ?, ?, ?)",
                 (lookup, to_store, skip_envs, hide_return_frames))
    conn.commit()
    conn.close()
    return lookup


def load(lookup) -> Union[Tuple, None]:
    conn = sqlite3.connect("saved")
    for row in conn.execute('SELECT * FROM stored_lines WHERE code=?', (lookup,)):
        return row[1:]
    conn.close()

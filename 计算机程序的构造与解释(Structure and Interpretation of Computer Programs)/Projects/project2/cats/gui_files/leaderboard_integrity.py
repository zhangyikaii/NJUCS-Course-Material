import base64
import json
import os
import random
import time
from functools import wraps
from queue import Queue
from threading import Thread

import cats

fernet = None

COMMON_WORDS_SET = set(cats.lines_from_file('data/common_words.txt'))
CAPTCHA_QUEUE_LEN = 200
CAPTCHA_LENGTH = 10
CAPTCHA_WORD_LEN = 6

captcha_queue = Queue()


def require_fernet(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        global fernet
        if not fernet:
            from cryptography.fernet import Fernet
            fernet = Fernet(os.environ.get("FERNET_KEY", Fernet.generate_key()))
        return f(*args, **kwargs)

    return wrapped


def token_writer(f):
    @wraps(f)
    @require_fernet
    def wrapped(*args, **kwargs):
        data = f(*args, **kwargs)
        decoded = json.dumps(data).encode("utf-8")
        return fernet.encrypt(decoded).decode("utf-8")
    return wrapped


def token_reader(fail):
    def decorator(f):
        @wraps(f)
        @require_fernet
        def wrapped(*, token, **kwargs):
            from cryptography.fernet import InvalidToken
            if not token:
                return fail
            try:
                return f(token=json.loads(fernet.decrypt(token.encode("utf-8"))), **kwargs)
            except (TypeError, InvalidToken):
                return fail
        return wrapped
    return decorator


@token_writer
def create_wpm_authorization(user, wpm):
    return {
        "user": user,
        "wpm": wpm,
    }


@token_reader(fail=0)
def get_authorized_limit(user, token):
    if token["user"] != user:
        return 0
    return token["wpm"]


@token_writer
def encode_challenge(user, words):
    return {
        "user": user,
        "words": words,
        "startTime": time.time(),
    }


@token_reader(fail=(False, False))
def decode_challenge(token):
    return token["user"], token["words"], token["startTime"]


def populate_captcha_queue():
    while captcha_queue.qsize() < CAPTCHA_QUEUE_LEN:
        captcha_queue.put(generate_captcha())


def generate_captcha():
    from claptcha import Claptcha
    word = random.choice([x for x in COMMON_WORDS_SET if len(x) < CAPTCHA_LENGTH])
    c = Claptcha(word, "gui_files/FreeMono.ttf", margin=(20, 10))
    image_b64 = base64.b64encode(c.bytes[1].getvalue()).decode("utf-8")
    return "data:image/png;base64," + image_b64, word


def get_captcha_urls(num_words=CAPTCHA_LENGTH):
    Thread(target=populate_captcha_queue).start()

    images, words = [], []
    for _ in range(num_words):
        image, word = captcha_queue.get()
        images.append(image)
        words.append(word)

    return images, words

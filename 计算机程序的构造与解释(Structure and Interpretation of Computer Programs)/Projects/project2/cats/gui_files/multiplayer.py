import time
from collections import namedtuple, defaultdict
from datetime import datetime, timedelta
from random import randrange

import cats
from gui_files.common_server import route, forward_to_server, server_only
from gui_files.db import connect_db, setup_db
from gui_files.leaderboard_integrity import get_authorized_limit, get_captcha_urls, encode_challenge, decode_challenge, \
    create_wpm_authorization

MIN_PLAYERS = 2
MAX_PLAYERS = 4
QUEUE_TIMEOUT = timedelta(seconds=1)
MAX_WAIT = timedelta(seconds=5)

MAX_NAME_LENGTH = 30

MAX_UNVERIFIED_WPM = 90
CAPTCHA_ACCURACY_THRESHOLD = 60
CAPTCHA_SLOWDOWN_FACTOR = 0.6


def db_init():
    setup_db("cats")
    with connect_db() as db:
        db(
            """CREATE TABLE IF NOT EXISTS leaderboard (
        name varchar(128),
        user_id varchar(128),
        wpm double,
        PRIMARY KEY (`user_id`)
    );"""
        )


def create_multiplayer_server():
    State = namedtuple("State", ["queue", "game_lookup", "game_data", "progress"])
    State = State({}, {}, {}, defaultdict(list))

    @route
    @server_only
    def provide_id():
        return randrange(1000000000)

    @route
    @forward_to_server
    def request_match(id):
        if id in State.game_lookup:
            game_id = State.game_lookup[id]
            return {
                    "start": True,
                    "text": State.game_data[game_id]["text"],
                    "players": State.game_data[game_id]["players"],
                }

        if id not in State.queue:
            State.queue[id] = [None, datetime.now()]

        State.queue[id][0] = datetime.now()

        to_remove = []

        for player, (recent_time, join_time) in State.queue.items():
            if datetime.now() - recent_time > QUEUE_TIMEOUT:
                to_remove.append(player)

        for player in to_remove:
            del State.queue[player]

        if len(State.queue) >= MAX_PLAYERS or \
                max(datetime.now() - join_time for recent_time, join_time in State.queue.values()) >= MAX_WAIT and \
                len(State.queue) >= MIN_PLAYERS:
            # start game!
            import gui
            curr_text = gui.request_paragraph()
            game_id = gui.request_id()

            for player in State.queue:
                State.game_lookup[player] = game_id

            queue = State.queue
            players = list(queue.keys())

            State.game_data[game_id] = {"text": curr_text, "players": players}

            for player in queue:
                State.progress[player] = [(0, time.time())]

            State.queue.clear()

            return {"start": True, "text": curr_text, "players": players}
        else:
            return {"start": False, "numWaiting": len(State.queue)}

    @route
    @server_only
    def set_progress(id, progress):
        """Record progress message."""
        State.progress[id].append((progress, time.time()))
        return ""

    @route
    @forward_to_server
    def request_progress(targets):
        now = {t: State.progress[t][-1] for t in targets}
        elapsed = [[now[t][0], now[t][1] - State.progress[t][0][1]] for t in targets]
        return elapsed

    @route
    @forward_to_server
    def request_all_progress(targets):
        return [State.progress[target] for target in targets]

    @route
    @forward_to_server
    def record_wpm(name, user, wpm, token):
        authorized_limit = get_authorized_limit(user=user, token=token)

        if wpm > max(MAX_UNVERIFIED_WPM, authorized_limit) or len(name) > MAX_NAME_LENGTH:
            return

        with connect_db() as db:
            db("DELETE FROM leaderboard WHERE user_id = (%s)", [user])
            db("INSERT INTO leaderboard (name, user_id, wpm) VALUES (%s, %s, %s)", [name, user, wpm])

    @route
    @forward_to_server
    def check_leaderboard_eligibility(wpm, user, token):
        with connect_db() as db:
            vals = db("SELECT wpm FROM leaderboard ORDER BY wpm DESC LIMIT 20").fetchall()
            threshold = vals[-1][0] if len(vals) >= 20 else 0
            prev_best = db("SELECT wpm FROM leaderboard WHERE user_id=(%s)", [user]).fetchone()
            if prev_best:
                threshold = max(threshold, prev_best[0])

        authorized_limit = get_authorized_limit(user=user, token=token)

        return {
            "eligible": wpm >= threshold,
            "needVerify": wpm > max(authorized_limit, MAX_UNVERIFIED_WPM)
        }

    @route
    @forward_to_server
    def request_wpm_challenge(user):
        captcha_image_urls, words = get_captcha_urls()
        token = encode_challenge(user, words)
        return {
            "images": captcha_image_urls,
            "token": token,
            "lastWordLen": len(words[-1])
        }

    @route
    @forward_to_server
    def claim_wpm_challenge(user, token, typed, claimed_wpm):
        challenge_user, reference, start_time = decode_challenge(token=token)
        end_time = time.time()

        if user != challenge_user:
            return

        accuracy = cats.accuracy(" ".join(typed), " ".join(reference))
        wpm = cats.wpm(" ".join(reference), end_time - start_time)

        if wpm < claimed_wpm * CAPTCHA_SLOWDOWN_FACTOR:
            # too slow!
            return {
                "success": False,
                "message": "Your captcha was typed too slowly!"
            }

        if accuracy < CAPTCHA_ACCURACY_THRESHOLD:
            # too inaccurate!
            return {
                "success": False,
                "message": "You made too many mistakes!"
            }

        return {
            "success": True,
            "token": create_wpm_authorization(user, claimed_wpm)
        }

    @route
    @forward_to_server
    def leaderboard():
        with connect_db() as db:
            return list(list(x) for x in db("SELECT name, wpm FROM leaderboard ORDER BY wpm DESC LIMIT 20").fetchall())

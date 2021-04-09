import os
from contextlib import contextmanager

from time import sleep

# noinspection PyUnresolvedReferences
import __main__

NUM_RETRIES = 5
SLEEP_DELAY = 2


def setup_db(service_name):
    from sqlalchemy import create_engine
    global engine
    engine = create_engine(os.getenv("DATABASE_URL", "mysql://localhost/{}".format(service_name)))


@contextmanager
def connect_db():
    from sqlalchemy.exc import OperationalError

    def db(*args):
        for _ in range(NUM_RETRIES):
            with engine.connect() as conn:
                try:
                    try:
                        if isinstance(args[1][0], str):
                            raise TypeError
                    except (IndexError, TypeError):
                        return conn.execute(*args)
                    else:
                        for data in args[1]:
                            conn.execute(args[0], data, *args[2:])
                except OperationalError as e:
                    print("MySQL Failure, retrying in {} seconds...".format(SLEEP_DELAY), e)
                    sleep(SLEEP_DELAY)
                    continue
                else:
                    break
        else:
            print("{} repeated failures, transaction failed".format(NUM_RETRIES))

    yield db

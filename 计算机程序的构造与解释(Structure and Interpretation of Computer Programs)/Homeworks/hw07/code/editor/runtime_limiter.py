import sys
import threading
import time

import log
from scheme_exceptions import TerminatedError


class OperationCanceledException(Exception):
    pass


class TimeLimitException(Exception):
    pass


def limiter(raise_exception, lim, func, *args):
    is_event = isinstance(lim, threading.Event)
    lim_is_set = lim.is_set if is_event else None  # For performance
    gettime = time.time  # For performance
    end = (gettime() + lim) if not is_event else None

    def tracer(*args):
        if lim_is_set() if is_event else gettime() > end:
            raise_exception(OperationCanceledException() if is_event else TimeLimitException())
        return tracer

    sys_tracer = sys.gettrace()
    try:
        sys.settrace(tracer)
        func(*args)
    finally:
        sys.settrace(sys_tracer)


def scheme_limiter(*args, **kwargs):
    def raise_(e):  # Translate to scheme exception and throw
        if isinstance(e, OperationCanceledException):
            e = TerminatedError
        raise e

    return limiter(raise_, *args, **kwargs)

try:
    import readline  # history and arrow keys for CLI
except ImportError:
    pass  # but not everyone has it
import sys

from reader import read
from expr import global_env

# program start
if __name__ == '__main__':
    """Run a read-eval-print loop.
    `python3 repl.py` to start an interactive REPL.
    `python3 repl.py --read` to interactively read expressions and
      print their Python representations.
    """
    read_only = len(sys.argv) == 2 and sys.argv[1] == '--read'

    while True:
        try:
            # `input` prints the prompt, waits, and returns the user's input.
            user_input = input('> ')
            expr = read(user_input)
            if expr is not None:
                if read_only:
                    print(repr(expr))
                else:
                    print(expr.eval(global_env))
        except (SyntaxError, NameError) as err:
            print(type(err).__name__ + ':', err)
        except (KeyboardInterrupt, EOFError):  # Ctrl-C, Ctrl-D
            print()  # blank line
            break  # exit while loop (and end program)
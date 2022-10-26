import time
from functools import wraps

from onliner_parser.utils import Font


def exec_time(start_text='Starting parsing...', end_text='Parsing completed!'):
    def wrapper(func):
        @wraps(func)
        def wrapped_wrapper(*args, **kwargs):
            start = time.time()
            print(f'{Font.INFO} {start_text}')
            func(*args, **kwargs)
            executing_time = time.strftime("%H:%M:%S", time.gmtime(round(time.time() - start, 2)))
            print(f'\n{Font.INFO} {end_text} Execution time: {executing_time}{Font.NORMAL}')
        return wrapped_wrapper
    return wrapper

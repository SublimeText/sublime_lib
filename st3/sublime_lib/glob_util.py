import re
from functools import lru_cache


GLOB_RE = re.compile(r'(\*\*/?|\*)')


@lru_cache()
def get_glob_expr(pattern):
    s = ''
    for part in GLOB_RE.split(pattern):
        if part == '**/':
            s += r'(?:.*/)?'
        elif part == '**':
            s += r'(?:.*)'
        elif part == '*':
            s += r'(?:[^/]*)'
        else:
            s += re.escape(part)

    return re.compile(r'\A' + s + r'\Z')

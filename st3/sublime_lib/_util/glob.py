import re
from functools import lru_cache

from .._compat.typing import Callable

__all__ = ['get_glob_matcher']


GLOB_RE = re.compile(r"""(?x)(
    \*
    | \?
    | \[ .*? \]
)""")


@lru_cache()
def get_glob_matcher(pattern: str) -> Callable[[str], bool]:
    if pattern.startswith('/'):
        pattern = pattern[1:]
    else:
        pattern = '**/' + pattern

    expr_string = r'\A'
    for component in pattern.split('/'):
        if component == '':
            pass
        elif component == '*':
            # Component must not be empty.
            expr_string += r'(?:[^/])+' + '/'
        elif component == '**':
            expr_string += r'(?:.*(?:\Z|/))?'
        elif '**' in component:
            raise ValueError("Invalid pattern: '**' can only be an entire path component")
        else:
            for part in GLOB_RE.split(component):
                if part == '':
                    pass
                elif part == '*':
                    expr_string += r'(?:[^/])*'
                elif part == '?':
                    expr_string += r'(?:[^/])'
                elif part[0] == '[':
                    expr_string += part
                else:
                    expr_string += re.escape(part)
            expr_string += '/'

    expr_string = expr_string.rstrip('/') + r'\Z'
    expr = re.compile(expr_string)

    return lambda path: (expr.search(path) is not None)

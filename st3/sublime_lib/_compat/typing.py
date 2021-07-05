import sys

if sys.version_info >= (3, 8, 0):
    from typing import *  # noqa: F401, F403
else:
    from .typing_stubs import *  # type: ignore # noqa: F401, F403

try:
    from enum import *  # noqa: F401, F403
except ImportError:
    from ..vendor.python.enum import *  # type: ignore # noqa: F401, F403

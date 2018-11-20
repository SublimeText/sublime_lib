from sublime import Region

from contextlib import contextmanager
from functools import wraps
from io import SEEK_SET, SEEK_CUR, SEEK_END, TextIOBase


def define_guard(guard_fn):
    def decorator(wrapped):
        @wraps(wrapped)
        def wrapper_guards(self, *args, **kwargs):
            ret_val = guard_fn(self)
            if hasattr(ret_val, '__enter__'):
                with ret_val:
                    return wrapped(self, *args, **kwargs)
            else:
                return wrapped(self, *args, **kwargs)

        return wrapper_guards

    return decorator


class ViewStream(TextIOBase):
    """A :class:`~io.TextIOBase` encapsulating a :class:`~sublime.View` object.

    All public methods (except :meth:`flush`) require that the underlying View object
    be valid (using :meth:`View.is_valid`). Otherwise, :class:`ValueError` will be raised.

    The :meth:`read`, :meth:`readline`, :meth:`write`, :meth:`print`, and
    :meth:`tell` methods require that the underlying View have exactly one
    selection, and that the selection is empty (i.e. a simple cursor).
    Otherwise, :class:`ValueError` will be raised.

    :argument force_writes: If ``True``, then :meth:`write` and :meth:`print`
    will write to the view even if it is read-only. Otherwise, those methods
    will raise :exc:`ValueError`.

    :argument follow_cursor: If ``True``, then any method that moves the
    cursor position will scroll the view to ensure that the new position is
    visible.
    """

    @define_guard
    @contextmanager
    def guard_read_only(self):
        if self.view.is_read_only():
            if self.force_writes:
                self.view.set_read_only(False)
                yield
                self.view.set_read_only(True)
            else:
                raise ValueError("The underlying view is read-only.")
        else:
            yield

    @define_guard
    @contextmanager
    def guard_auto_indent(self):
        settings = self.view.settings()
        if settings.get('auto_indent'):
            settings.set('auto_indent', False)
            yield
            settings.set('auto_indent', True)
        else:
            yield

    @define_guard
    def guard_validity(self):
        if not self.view.is_valid():
            raise ValueError("The underlying view is invalid.")

    @define_guard
    def guard_selection(self):
        if len(self.view.sel()) == 0:
            raise ValueError("The underlying view has no selection.")
        elif len(self.view.sel()) > 1:
            raise ValueError("The underlying view has multiple selections.")
        elif not self.view.sel()[0].empty():
            raise ValueError("The underlying view's selection is not empty.")

    def __init__(self, view, *, force_writes=False, follow_cursor=False):
        self.view = view
        self.force_writes = force_writes
        self.follow_cursor = follow_cursor

    @guard_validity
    @guard_selection
    def read(self, size):
        """Read and return at most `size` characters from the stream as a
        single :class:`str`. If `size` is negative or None, reads until EOF.
        """
        begin = self._tell()
        end = self.view.size()

        return self._read(begin, end, size)

    @guard_validity
    @guard_selection
    def readline(self, size=-1):
        """Read until newline or EOF and return a single :class:`str`. If the stream is
        already at EOF, an empty string is returned.
        """
        begin = self._tell()
        end = self.view.full_line(begin).end()

        return self._read(begin, end, size)

    def _read(self, begin, end, size):
        if size is not None and size >= 0:
            end = min(end, begin + size)

        self._seek(end)
        return self.view.substr(Region(begin, end))

    @guard_validity
    @guard_selection
    @guard_read_only
    @guard_auto_indent
    def write(self, s):
        """Insert the string `s` into the view and return the number of
        characters inserted. The string will be inserted immediately before the
        cursor. It will not be auto-indented.

        Note: Because Sublime may convert tabs to spaces, the number of
        characters inserted may not match the length of the argument.
        """
        old_size = self.view.size()
        self.view.run_command('insert', {'characters': s})
        self._maybe_show_cursor()
        return self.view.size() - old_size

    def print(self, *objects, sep=' ', end='\n'):
        """Shorthand for :func:`print()` passing this ViewStream as the `file`
        argument."""
        print(*objects, file=self, sep=sep, end=end)
        self._maybe_show_cursor()

    def flush(self):
        """Do nothing. (The stream is not buffered.)"""
        pass

    @guard_validity
    def seek(self, offset, whence=SEEK_SET):
        """Move the cursor in the view to the given offset. If `whence` is
        provided, the behavior is the same as for TextIOBase. If the view had
        multiple selections, none will be preserved.
        """
        if whence == SEEK_SET:
            return self._seek(offset)
        elif whence == SEEK_CUR:
            if offset != 0:
                raise TypeError('Argument "offset" must be zero when "whence" '
                                'is io.SEEK_CUR.')
            # Don't move.
            self._maybe_show_cursor()
            return self._tell()
        elif whence == SEEK_END:
            if offset != 0:
                raise TypeError('Argument "offset" must be zero when "whence" '
                                'is io.SEEK_END.')
            return self._seek(self.view.size())
        else:
            raise TypeError('Invalid value for argument "whence".')

    def _seek(self, offset):
        selection = self.view.sel()
        selection.clear()
        selection.add(Region(offset))
        self._maybe_show_cursor()
        return offset

    @guard_validity
    def seek_start(self):
        """Move the cursor in the view to before the first character."""
        self._seek(0)

    @guard_validity
    def seek_end(self):
        """Move the cursor in the view to after the last character."""
        self._seek(self.view.size())

    @guard_validity
    @guard_selection
    def tell(self):
        """Return the character offset of the cursor."""
        return self._tell()

    def _tell(self):
        return self.view.sel()[0].b

    @guard_validity
    @guard_selection
    def show_cursor(self):
        """Scroll the view to show the position of the cursor."""
        self._show_cursor()

    def _show_cursor(self):
        self.view.show(self._tell())

    def _maybe_show_cursor(self):
        if self.follow_cursor:
            self._show_cursor()

    @guard_validity
    @guard_selection
    @guard_read_only
    def clear(self):
        """Erase all text in the view."""
        self.view.run_command('select_all')
        self.view.run_command('left_delete')

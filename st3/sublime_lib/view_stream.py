from sublime import Region
from io import SEEK_SET, SEEK_CUR, SEEK_END, TextIOBase


class ViewStream(TextIOBase):
    """A TextIO encapsulating a `sublime.View` object.

    All public methods (except flush) require that the underlying View object
    be valid (using View.is_valid). Otherwise, ValueError will be raised.

    The `read`, `readline`, `write`, and `tell` methods require that the
    underlying View have exactly one selection, and that the selection is
    empty (i.e. a simple cursor). Otherwise, ValueError will be raised.
    """

    def __init__(self, view):
        self.view = view

    def _check_selection(self):
        if len(self.view.sel()) == 0:
            raise ValueError("The underlying view has no selection.")
        elif len(self.view.sel()) > 1:
            raise ValueError("The underlying view has multiple selections.")
        elif not self.view.sel()[0].empty():
            raise ValueError("The underlying view's selection is not empty.")

    def _check_is_valid(self):
        if not self.view.is_valid():
            raise ValueError("The underlying view is invalid.")

    def read(self, size):
        """Read and return at most <var>size</var> characters from the stream as a
        single `str`. If <var>size</var> is negative or None, reads until EOF.
        """

        self._check_is_valid()
        self._check_selection()

        begin = self._tell()
        end = self.view.size()

        return self._read(begin, end, size)

    def readline(self, size=-1):
        """Read until newline or EOF and return a single `str`. If the stream is
        already at EOF, an empty string is returned.
        """

        self._check_is_valid()
        self._check_selection()

        begin = self._tell()
        end = self.view.full_line(begin).end()

        return self._read(begin, end, size)

    def _read(self, begin, end, size):
        if size is not None and size >= 0:
            end = min(end, begin + size)

        self._seek(end)
        return self.view.substr(Region(begin, end))

    def write(self, s):
        """Insert the string <var>s</var> into the view and return the number of
        characters inserted. The string will be inserted immediately before the
        cursor.
        """

        self._check_is_valid()
        self._check_selection()
        self.view.run_command('insert', {'characters': s})
        return len(s)

    def print(self, *objects, **kwargs):
        print(*objects, file=self, **kwargs)

    def flush(self):
        """Do nothing. (The stream is not buffered.)"""
        pass

    def seek(self, offset, whence=SEEK_SET):
        """Move the cursor in the view to the given offset. If `whence` is
        provided, the behavior is the same as for TextIOBase. If the view had
        multiple selections, none will be preserved.
        """

        self._check_is_valid()

        if whence == SEEK_SET:
            return self._seek(offset)
        elif whence == SEEK_CUR:
            if offset != 0:
                raise TypeError('Argument "offset" must be zero when "whence" '
                                'is io.SEEK_CUR.')
            # Don't move.
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
        return offset

    def seek_start(self):
        """Move the cursor in the view to before the first character."""
        self._check_is_valid()
        self._seek(0)

    def seek_end(self):
        """Move the cursor in the view to after the last character."""
        self._check_is_valid()
        self._seek(self.view.size())

    def tell(self):
        """Return the character offset of the cursor."""
        self._check_is_valid()
        self._check_selection()
        return self._tell()

    def _tell(self):
        return self.view.sel()[0].b

    def clear(self):
        """Erase all text in the view."""
        self._check_is_valid()
        self.view.run_command('select_all')
        self.view.run_command('left_delete')

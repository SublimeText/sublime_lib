from sublime import Region
from io import SEEK_SET, SEEK_CUR, SEEK_END, TextIOBase, UnsupportedOperation

"""A writable text stream encapsulating a `sublime.View` object."""
class ViewStream(TextIOBase):
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

    """Insert the string <var>s</var> into the view and return the number of
    characters inserted. The string will be inserted immediately before the
    cursor.

    @precondition: The view is valid. (ValueError)
    @precondition: The view has exactly one selection. (ValueError)
    """
    def write(self, s):
        self._check_is_valid()
        self._check_selection()
        self.view.run_command('insert', { 'characters': s })
        return len(s)

    def print(self, *objects, **kwargs):
        print(*objects, file=self, **kwargs)

    """Do nothing."""
    def flush(self):
        pass

    """Move the cursor in the view to the given index. If `whence` is provided,
    the behavior is the same as for TextIOBase. If the view had multiple
    selections, none will be preserved.

    @precondition: The view is valid. (ValueError)
    """
    def seek(self, index, whence=SEEK_SET):
        self._check_is_valid()
        if whence == SEEK_SET:
            self._seek(index)
        elif whence == SEEK_CUR:
            if index != 0: raise TypeError('Argument "index" must be zero when "whence" is io.SEEK_CUR.')
            pass # Do nothing.
        elif whence == SEEK_END:
            if index != 0: raise TypeError('Argument "index" must be zero when "whence" is io.SEEK_END.')
            self._seek(self.view.size())
        else:
            raise TypeError('Invalid value for argument "whence".')

    def _seek(self, index):
        selection = self.view.sel()
        selection.clear()
        selection.add(Region(index))

    """Move the cursor in the view to before the first character.

    @precondition: The view is valid. (ValueError)
    """
    def seek_start(self):
        self._check_is_valid()
        self._seek(0)

    """Move the cursor in the view to after the last character.

    @precondition: The view is valid. (ValueError)
    """
    def seek_end(self):
        self._check_is_valid()
        self._seek(self.view.size())

    def tell(self):
        self._check_is_valid()
        self._check_selection()
        return self.view.sel()[0].b


    """Erase all text in the view.

    @precondition: The view is valid. (ValueError)
    """
    def clear(self):
        self._check_is_valid()
        self.view.run_command('select_all')
        self.view.run_command('left_delete')

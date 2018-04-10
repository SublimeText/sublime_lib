from sublime import Region
from io import SEEK_SET, SEEK_CUR, SEEK_END

class ViewStream():
    def __init__(self, view):
        self.view = view

    def _check_selection(self):
        if len(self.view.sel()) == 0:
            raise ValueError("The underlying view has no selection.")
        if len(self.view.sel()) > 1:
            raise ValueError("The underlying view has multiple selections.")

    def _check_is_valid(self):
        if not self.view.is_valid():
            raise ValueError("The underlying view is invalid.")

    def write(self, s):
        self._check_is_valid()
        self._check_selection()
        self.view.run_command('insert', { 'characters': s })
        return len(s)

    def print(self, *objects, **kwargs):
        print(*objects, file=self, **kwargs)

    def flush(self):
        pass

    def seek(self, index, whence=SEEK_SET):
        self._check_is_valid()
        if whence == SEEK_SET:
            selection = self.view.sel()
            selection.clear()
            selection.add(Region(index))
        elif whence == SEEK_CUR:
            if index != 0: raise TypeError('Argument "index" must be zero when "whence" is io.SEEK_CUR.')
            pass # Do nothing.
        elif whence == SEEK_END:
            if index != 0: raise TypeError('Argument "index" must be zero when "whence" is io.SEEK_END.')
            self.seek(self.view.size())
        else:
            raise TypeError('Invalid value for argument "whence".')

    def seek_start(self):
        self.seek(0)

    def seek_end(self):
        self.seek(self.view.size())

    def clear(self):
        self._check_is_valid()
        self.view.run_command('select_all')
        self.view.run_command('left_delete')

from sublime import Region
from io import SEEK_SET, SEEK_CUR, SEEK_END

class ViewStream():
    def __init__(self, view):
        self.view = view

    def write(self, s):
        self.view.run_command('insert', { 'characters': s })
        return len(s)

    def print(self, *objects, **kwargs):
        print(*objects, file=self, **kwargs)

    def flush(self):
        pass

    def seek(self, index, whence=SEEK_SET):
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
        self.view.run_command('select_all')
        self.view.run_command('left_delete')

from sublime import Region

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

    def seek(self, index):
        selection = self.view.sel()
        selection.clear()
        selection.add(Region(index))

    def seek_start(self):
        self.seek(0)

    def seek_end(self):
        self.seek(self.view.size())

    def clear(self):
        self.view.run_command('select_all')
        self.view.run_command('left_delete')

from sublime import Region


class ViewBuffer():
    def __init__(self, view):
        self.view = view
        self._size = None
        self._text = None

    @property
    def size(self):
        if self._size is None:
            self._size = self.view.size()
        return self._size

    @property
    def text(self):
        if self._text is None:
            self._text = self.view.substr(Region(0, self.size))
        return self._text

    def invalidate(self):
        self._size = None
        self._text = None

    def __getitem__(self, arg):
        if isinstance(arg, Region):
            return self.text[arg.begin():arg.end()]
        else:
            return self.text[arg]

    def split_indent(self, region):
        i = region.begin()
        while self[i].isspace() and self[i] != '\n':
            i += 1
        return (Region(region.begin(), i), Region(i, region.end()))

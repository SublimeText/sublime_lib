from sphinx.ext.autodoc.mock import _MockObject

import sys


class MockType(_MockObject):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name


class SublimePluginMock:
    EventListener = MockType('sublime_plugin.EventListener')
    ViewEventListener = MockType('sublime_plugin.ViewEventListener')


sys.modules[__name__] = SublimePluginMock()

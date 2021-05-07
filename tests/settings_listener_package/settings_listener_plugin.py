import sublime_lib
from sublime_lib import on_setting_changed, ResourcePath


__all__ = ['FooSettingListener', 'GlobalFooSettingListener']


PACKAGE_NAME = ResourcePath.from_file_path(__file__).package


class FooSettingListener(sublime_lib.ViewSettingsListener):
    @on_setting_changed('foo')
    def foo_changed(self, new_value: object, old_value: object):
        changes = self.settings.get('changes', [])
        self.settings.set('changes', changes + [[new_value, old_value]])


class GlobalFooSettingListener(sublime_lib.GlobalSettingsListener):
    SETTINGS_NAME = PACKAGE_NAME + '.sublime-settings'

    @on_setting_changed('foo')
    def foo_changed(self, new_value: object, old_value: object):
        changes = self.settings.get('changes', [])
        self.settings.set('changes', changes + [[new_value, old_value]])

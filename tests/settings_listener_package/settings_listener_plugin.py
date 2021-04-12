from sublime_lib import ViewSettingsListener, GlobalSettingsListener, on_setting_changed


__all__ = ['FooSettingListener', 'GlobalFooSettingListener']


class FooSettingListener(ViewSettingsListener):
    @on_setting_changed('foo')
    def foo_changed(self, new_value: object, old_value: object):
        changes = self.settings.get('changes', [])
        self.settings.set('changes', changes + [[new_value, old_value]])
        print('foo_changed', new_value, old_value, changes)


class GlobalFooSettingListener(GlobalSettingsListener):
    SETTINGS_NAME = 'Baz.sublime-settings'

    @on_setting_changed('foobar')
    def foo_changed(self, new_value: object, old_value: object):
        print('foo_changed', new_value, old_value)

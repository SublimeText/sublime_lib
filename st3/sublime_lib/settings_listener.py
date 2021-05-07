import sublime
import sublime_plugin

from collections import namedtuple

from ._util.weak_method import weak_method
from ._util.collections import get_selector


from ._compat.typing import Callable, Any, Iterator, Tuple, TypeVar, Union


__all__ = ['GlobalSettingsListener', 'ViewSettingsListener', 'on_setting_changed']


OnChangedOptions = namedtuple('OnChangedOptions', ('selector'))
OPTIONS_ATTRIBUTE = '_sublime_lib_settings_listener_options'


class BaseSettingsListener:
    def _handlers(self) -> Iterator[Tuple[str, Callable, OnChangedOptions]]:
        for name in dir(self):
            value = getattr(self, name)
            options = getattr(value, OPTIONS_ATTRIBUTE, None)

            if not name.startswith('_') and options is not None:
                yield name, value, options

    def __init__(self, settings: sublime.Settings, *args: Any, **kwargs: Any) -> None:
        # Don't complain that object.__init__ doesn't take any args
        super().__init__(*args, **kwargs)  # type: ignore
        self.settings = settings

        self.settings.add_on_change(str(id(self)), weak_method(self._on_settings_changed))

        self._last_known_values = {
            name: options.selector(self.settings)
            for name, _, options in self._handlers()
        }

    def __del__(self) -> None:
        self.settings.clear_on_change(str(id(self)))

    def _on_settings_changed(self) -> None:
        for name, handler, options in self._handlers():
            previous_value = self._last_known_values[name]
            current_value = options.selector(self.settings)

            if current_value != previous_value:
                self._last_known_values[name] = current_value
                handler(current_value, previous_value)


class GlobalSettingsListener(BaseSettingsListener, sublime_plugin.EventListener):
    """
    A subclass of :class:`sublime_plugin.EventListener`
    that also listens for changes in a global settings object.

    Subclasses must set the `SETTINGS_NAME` class variable to the name of the global settings.

    Example usage:

    .. code-block:: python

        from sublime_lib import GlobalSettingsListener, on_setting_changed

        class JsCustomConfigurationsListener(GlobalSettingsListener)
            SETTINGS_NAME = 'JS Custom.sublime-settings'

            @on_setting_changed('configurations')
            def configurations_changed(self, new_configuration, old_configuration):
                if self.settings.get('auto_build', False):
                    sublime.active_window().run_command('build_js_custom_syntaxes')
    """
    SETTINGS_NAME = ''

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(sublime.load_settings(self.SETTINGS_NAME), *args, **kwargs)

    def _on_settings_changed(self) -> None:
        # Necessary because Sublime keeps EventListener objects alive unnecessarily.
        # See https://github.com/sublimehq/sublime_text/issues/4078.
        if self in sublime_plugin.all_callbacks['on_new']:
            super()._on_settings_changed()
        else:
            self.settings.clear_on_change(str(id(self)))

    def on_new(self, view: sublime.View) -> None:
        pass


class ViewSettingsListener(BaseSettingsListener, sublime_plugin.ViewEventListener):
    """
    A subclass of :class:`sublime_plugin.ViewEventListener`
    that also listens for changes in the view settings.

    Example:

    .. code-block:: python

        from sublime_lib import ViewSettingsListener, on_setting_changed

        class TabSizeListener(ViewSettingsListener):
            @classmethod
            def is_applicable(cls, settings):
                return settings.get('translate_tabs_to_spaces', False)

            @classmethod
            def applies_to_primary_view_only(cls):
                return True

            @on_setting_changed('tab_size')
            def tab_size_changed(self, new_value, old_value):
                self.view.run_command('resize_existing_tabs', {
                    'new_size': new_value,
                    'old_size': old_value,
                })
    """
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        view = args[0]
        assert isinstance(view, sublime.View)
        super().__init__(view.settings(), *args, **kwargs)


Selected = TypeVar('Selected')
OnChangeListener = Callable[[BaseSettingsListener, Selected, Selected], None]


def on_setting_changed(
    selector: Union[str, Callable[[sublime.Settings], Selected]]
) -> Callable[[OnChangeListener], OnChangeListener]:
    """
    A decorator function to mark a method
    of a :class:`GlobalSettingsListener` or :class:`ViewSettingsListener`
    as a setting change handler.

    The handler is not called every time the `settings` object changes,
    but only when the value derived using the `selector` argument changes.
    If `selector` is callable, then the derived value is ``selector(self)``.
    If `selector` is a :class:`str`,
    then the derived value is ``self.get(selector, None)``.
    Otherwise, the derived value is ``projection(self, selector)``.

    The handler should accept two arguments:
    the new derived value and the previous derived value.
    """
    def decorator(function: OnChangeListener) -> OnChangeListener:
        setattr(function, OPTIONS_ATTRIBUTE, OnChangedOptions(get_selector(selector)))
        return function

    return decorator

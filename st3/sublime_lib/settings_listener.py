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
    SETTINGS_NAME = ''

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(sublime.load_settings(self.SETTINGS_NAME), *args, **kwargs)


class ViewSettingsListener(BaseSettingsListener, sublime_plugin.ViewEventListener):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        view = args[0]
        assert isinstance(view, sublime.View)
        super().__init__(view.settings(), *args, **kwargs)


Selected = TypeVar('Selected')
OnChangeListener = Callable[[BaseSettingsListener, Selected, Selected], None]


def on_setting_changed(
    selector: Union[str, Callable[[sublime.Settings], Selected]]
) -> Callable[[OnChangeListener], OnChangeListener]:
    def decorator(function: OnChangeListener) -> OnChangeListener:
        setattr(function, OPTIONS_ATTRIBUTE, OnChangedOptions(get_selector(selector)))
        return function

    return decorator

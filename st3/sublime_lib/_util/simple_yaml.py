import sublime
import re


__all__ = ['parse_simple_top_level_keys']


def parse_simple_top_level_keys(text):
    return dict(
        map(_parse_yaml_value, match.groups())
        for match in re.finditer(r'(?m)^([^\s#].*?\s*): *(.+) *$', text)
    )


def _parse_yaml_value(value):
    if value.startswith("'"):
        return value[1:-1].replace("''", "'")
    elif value.startswith('"'):
        # JSON and YAML quotation rules are very similar, if not identical
        return sublime.decode_value(value)
    elif value == "true":
        return True
    elif value == "false":
        return False
    elif value == "null":
        return None
    else:
        # Does not handle numbers because we don't expect any
        return value

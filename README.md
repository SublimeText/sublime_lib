# sublime_lib

A utility library for Sublime Text, 
providing a variety of convenience features.

## Installation

To make use of sublime_lib in a package...

1. declare it as [dependency](https://packagecontrol.io/docs/dependencies):

   Create a file named `dependencies.json`
   with the following contents in package's root directory:

   ```json
   {
       "*": {
           "*": [
               "sublime_lib"
           ]
       }
   }
   ```

   Open _Command Palette_ and run `Package Control: Satisfy Libraries`
   to ensure sublime_lib is installed and available for use.

2. Import sublime_lib in plugins, which want to make use of it.

   ```python
   import sublime_lib
   ```

## Features

For complete documentation of all features,
see the [API documentation](https://sublimetext.github.io/sublime_lib/).

Highlights include:

- [`ActivityIndicator`](https://sublimetext.github.io/sublime_lib/#activity-indicator) context manager to indicate background activity via status bar.
- [`ResourcePath`](https://sublimetext.github.io/sublime_lib/#sublime_lib.ResourcePath), a [pathlib.Path](https://docs.python.org/3/library/pathlib.html) inspired representation of ST's resource paths,
  with methods to convert from and to filesystem paths.
- [`SettingsDict`](https://sublimetext.github.io/sublime_lib/modules/sublime_lib.settings_dict.html) provides a standard Python `dict` inspired interface for `sublime.Settings` objects.
- [`OutputPanel`](https://sublimetext.github.io/sublime_lib/modules/sublime_lib.output_panel.html), extending `ViewStream` to provide additional functionality for output panel views.
- [`ViewStream`](https://sublimetext.github.io/sublime_lib/modules/sublime_lib.view_stream.html), a standard [Python IO stream](https://docs.python.org/3/library/io.html#io.TextIOBase) wrapping a `sublime.View` object

### Deprecated

The [`flags` submodule](https://sublimetext.github.io/sublime_lib/#module-sublime_lib.flags) is deprecated in favour of native API, available as of ST4135.

The [`syntax` submodule](https://sublimetext.github.io/sublime_lib/modules/sublime_lib.syntax.html), is marked deprecated in favour of native API functions, available as of ST4.

## Releasing a new version

1. Create a tag in the format `v<major>.<minor>.<patch>`
2. Push the tag to origin.

A GitHub action should be created that builds a WHEEL file,
creates a release for this tag
and attaches the WHEEL file as an artefact.

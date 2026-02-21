# sublime_lib

A utility library for Sublime Text,
providing a variety of convenience features.

## Installation

To make use of sublime_lib in a package...

1. declare it as [a dependency][pc-dependencies]:

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

2. Import sublime_lib in plugins which want to make use of it.

   ```python
   import sublime_lib
   ```

## Features

For complete documentation of all features,
see the [API documentation][docs].

Highlights include:

- [`ActivityIndicator`][sublime_lib.ActivityIndicator] context manager
  to indicate background activity via status bar.
- [`ResourcePath`][sublime_lib.ResourcePath],
  a [pathlib.Path][]-inspired representation of ST's resource paths
  with methods to convert from and to filesystem paths.
- [`SettingsDict`][sublime_lib.SettingsDict] provides a standard Python `dict`-like interface
  for `sublime.Settings` objects.
- [`ViewStream`][sublime_lib.ViewStream],
  providing a standard [Python IO stream][io.TextIOBase]
  wrapping a `sublime.View` object.
- [`OutputPanel`][sublime_lib.OutputPanel],
  extending `ViewStream` to provide additional functionality for output panel views.

### Deprecated

The [`flags` submodule][sublime_lib.flags] is deprecated
in favour of native API,
available as of ST4135.

The [Syntax Utilities][] are marked deprecated
in favour of native API functions,
available as of ST4.

## Releasing a new version

1. Create a tag in the format `v<major>.<minor>.<patch>`
2. Push the tag to origin.

A GitHub action builds a WHEEL file,
creates a release for this tag,
and attaches the WHEEL file as an artifact.

[docs]: https://sublimetext.github.io/sublime_lib/
[io.TextIOBase]: https://docs.python.org/3/library/io.html#io.TextIOBase
[pathlib.Path]: https://docs.python.org/3/library/pathlib.html
[pc-dependencies]: https://packagecontrol.io/docs/dependencies
[sublime_lib.ActivityIndicator]: https://sublimetext.github.io/sublime_lib/#sublime_lib.ActivityIndicator
[sublime_lib.flags]: https://sublimetext.github.io/sublime_lib/#module-sublime_lib.flags
[sublime_lib.OutputPanel]: https://sublimetext.github.io/sublime_lib/#sublime_lib.OutputPanel
[sublime_lib.ResourcePath]: https://sublimetext.github.io/sublime_lib/#sublime_lib.ResourcePath
[sublime_lib.SettingsDict]: https://sublimetext.github.io/sublime_lib/#sublime_lib.SettingsDict
[sublime_lib.ViewStream]: https://sublimetext.github.io/sublime_lib/#sublime_lib.ViewStream
[Syntax Utilities]: https://sublimetext.github.io/sublime_lib/#syntax-utilities

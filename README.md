# sublime_lib

An unofficial "standard library" for Sublime Text. Provides a variety of useful convenience features for other packages.

## Installation

To make use of sublime_lib in your own package, first declare it as a [dependency](https://packagecontrol.io/docs/dependencies) of your package. Create a file named `dependencies.json` in the root of your package with the following contents:

```json
{
    "*": {
        "*": [
            "sublime_lib"
        ]
    }
}
```

Then, anywhere in your package, you can import sublime_lib by name:

```python
import sublime_lib
```

## Features

For complete documentation of all features, see the [API documentation](https://sublimetext.github.io/sublime_lib/).

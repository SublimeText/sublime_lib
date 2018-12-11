:mod:`sublime_lib` API
======================

Contents
--------

.. container:: table-of-contents

  * `Settings dictionaries <#settings-dictionaries>`__

    * :class:`~sublime_lib.SettingsDict`
    * :class:`~sublime_lib.NamedSettingsDict`

  * `Output streams <#output-streams>`__

    * :class:`~sublime_lib.ViewStream`
    * :class:`~sublime_lib.OutputPanel`

  * `Resource paths <#resource-paths>`__

    * :class:`~sublime_lib.ResourcePath`

  * `View utilities <#view-utilities>`__

    * :func:`~sublime_lib.new_view`
    * :func:`~sublime_lib.close_view`

  * `Window utilities <#window-utilities>`__

    * :func:`~sublime_lib.new_window`
    * :func:`~sublime_lib.close_window`
    * :func:`~sublime_lib.show_selection_panel`

  * `Syntax utilities <#syntax-utilities>`__

    * :func:`~sublime_lib.list_syntaxes`
    * :func:`~sublime_lib.get_syntax_for_scope`

  * :mod:`~sublime_lib.encodings` submodule

    * :func:`~sublime_lib.encodings.from_sublime`
    * :func:`~sublime_lib.encodings.to_sublime`

  * :mod:`~sublime_lib.flags` submodule

    * :mod:`~sublime_lib.flags`

Settings dictionaries
---------------------

.. autoclass:: sublime_lib.SettingsDict
.. autoclass:: sublime_lib.NamedSettingsDict

Output streams
--------------

.. autoclass:: sublime_lib.ViewStream
.. autoclass:: sublime_lib.OutputPanel

Resource paths
--------------

.. autoclass:: sublime_lib.ResourcePath

View utilities
--------------

.. autofunction:: sublime_lib.new_view
.. autofunction:: sublime_lib.close_view

Window utilities
----------------

.. autofunction:: sublime_lib.new_window
.. autofunction:: sublime_lib.close_window
.. autofunction:: sublime_lib.show_selection_panel

Syntax utilities
----------------

.. autofunction:: sublime_lib.list_syntaxes
.. autofunction:: sublime_lib.get_syntax_for_scope

:mod:`~sublime_lib.encodings` submodule
---------------------------------------

.. automodule:: sublime_lib.encodings

:mod:`~sublime_lib.flags` submodule
-----------------------------------

.. automodule:: sublime_lib.flags

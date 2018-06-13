def projection(d, keys):
    """
    Return a new :class:`dict` with keys restricted to values in `keys`.

    .. code-block:: python

       >>> projection({'a': 1, 'b': 2}, ['b'])
       {'b': 2}

    If `keys` is a :class:`dict`, then it maps keys of the original dict to
    keys of the result:

    .. code-block:: python

       >>> projection({'a': 1, 'b': 2}, {'b': 'c'})
       {'c': 2}
    """
    if isinstance(keys, dict):
        return {
            new_key: d[original_key]
            for original_key, new_key in keys.items()
            if original_key in d
        }
    else:
        return {
            key: d[key]
            for key in keys
            if key in d
        }

def __getattr__(key):
    if key.isupper():
        return hash(key)
    else:
        return 'sublime.'+key

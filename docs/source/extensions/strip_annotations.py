from sphinx.util.inspect import stringify_signature

import inspect


__all__ = ['strip_annotations']


def strip_annotations(
    app,
    what: str,
    name: str,
    obj,
    options,
    signature,
    return_annotation
):
    if what not in {'function', 'method', 'class'}:
        return

    original_signature = inspect.signature(obj)
    new_signature = original_signature.replace(
        return_annotation=inspect.Signature.empty,
        parameters=[
            param.replace(annotation=inspect.Parameter.empty)
            for param in original_signature.parameters.values()
            if param.name != 'self'
        ],
    )

    return stringify_signature(new_signature), None

"""Helpers for the nTop Python Console. The code lives next to this file; after
editing it, run utils.reload() (no need to re-import).

    >>> from utils import summary
    >>> summary()                                    # the open notebook
    >>> summary(r"C:\\path\\part.ntop", restore=True) # a file, then reopen what was open
    >>> summary(md=r"C:\\temp\\blocks.md")            # also save as Markdown
"""
import importlib as _il

import summary as _bs


def reload():
    """Re-read the helper modules after editing them."""
    _il.reload(_bs)
    summary.__doc__ = _bs.__doc__


def summary(*args, **kwargs):
    return _bs.summary(*args, **kwargs)


summary = summary  # older name
summary.__doc__ = _bs.__doc__

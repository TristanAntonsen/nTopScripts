"""Helpers for the nTop Python Console. Loads the repo copies below, so edits there
take effect after ntop_utils.reload() - nothing to copy here.

    >>> from ntop_utils import block_summary
    >>> block_summary()                                   # the open notebook
    >>> block_summary(r"C:\\path\\part.ntop", restore=True) # a file, then reopen what was open
"""
import importlib.util as _ilu

_SCRIPTS = r"C:\Users\tristanantonsen\Desktop\code\ntop-api-skills\skills\ntop-notebook-api\scripts"


def _load(name):
    # Load by path rather than adding _SCRIPTS to sys.path: that folder also holds
    # scripts that run on import (summarize_graph.py).
    spec = _ilu.spec_from_file_location(name, _SCRIPTS + "\\" + name + ".py")
    mod = _ilu.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


_bs = None


def reload():
    """Re-read the repo copies after editing them (no need to re-import afterwards)."""
    global _bs
    _bs = _load("block_summary")


def block_summary(*args, **kwargs):
    return _bs.block_summary(*args, **kwargs)


reload()
block_summary.__doc__ = _bs.__doc__

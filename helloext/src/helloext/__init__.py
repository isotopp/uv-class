from __future__ import annotations

__all__ = ["hellop", "hellos"]


def hellop(*args, **kwargs):
    from ._hello import hellop as _hellop

    return _hellop(*args, **kwargs)


def hellos(*args, **kwargs):
    from ._hello import hellos as _hellos

    return _hellos(*args, **kwargs)

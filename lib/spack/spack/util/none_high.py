"""
Functions for comparing values that may potentially be None.
These none_high functions consider None as greater than all other values.
"""

# Preserve builtin min and max functions
_builtin_min = min
_builtin_max = max


def lt(lhs, rhs):
    """Less-than comparison.  None is greater than any value."""
    return lhs != rhs and (rhs is None or (lhs is not None and lhs < rhs))


def le(lhs, rhs):
    """Less-than-or-equal comparison.  None is greater than any value."""
    return lhs == rhs or lt(lhs, rhs)


def gt(lhs, rhs):
    """Greater-than comparison.  None is greater than any value."""
    return lhs != rhs and not lt(lhs, rhs)


def ge(lhs, rhs):
    """Greater-than-or-equal comparison.  None is greater than any value."""
    return lhs == rhs or gt(lhs, rhs)


def min(lhs, rhs):
    """Minimum function where None is greater than any value."""
    if lhs is None:
        return rhs
    elif rhs is None:
        return lhs
    else:
        return _builtin_min(lhs, rhs)


def max(lhs, rhs):
    """Maximum function where None is greater than any value."""
    if lhs is None or rhs is None:
        return None
    else:
        return _builtin_max(lhs, rhs)

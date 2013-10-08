"""
Functions for comparing values that may potentially be None.
These none_low functions consider None as less than all other values.
"""

# Preserve builtin min and max functions
_builtin_min = min
_builtin_max = max


def lt(lhs, rhs):
    """Less-than comparison.  None is lower than any value."""
    return lhs != rhs and (lhs == None or (rhs != None and lhs < rhs))


def le(lhs, rhs):
    """Less-than-or-equal comparison.  None is less than any value."""
    return lhs == rhs or lt(lhs, rhs)


def gt(lhs, rhs):
    """Greater-than comparison.  None is less than any value."""
    return lhs != rhs and not lt(lhs, rhs)


def ge(lhs, rhs):
    """Greater-than-or-equal comparison.  None is less than any value."""
    return lhs == rhs or gt(lhs, rhs)


def min(lhs, rhs):
    """Minimum function where None is less than any value."""
    if lhs == None or rhs == None:
        return None
    else:
        return _builtin_min(lhs, rhs)


def max(lhs, rhs):
    """Maximum function where None is less than any value."""
    if lhs == None:
        return rhs
    elif rhs == None:
        return lhs
    else:
        return _builtin_max(lhs, rhs)

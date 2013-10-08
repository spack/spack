"""
Functions for comparing values that may potentially be None.
Functions prefixed with 'none_low_' treat None as less than all other values.
Functions prefixed with 'none_high_' treat None as greater than all other values.
"""

def none_low_lt(lhs, rhs):
    """Less-than comparison.  None is lower than any value."""
    return lhs != rhs and (lhs == None or (rhs != None and lhs < rhs))


def none_low_le(lhs, rhs):
    """Less-than-or-equal comparison.  None is less than any value."""
    return lhs == rhs or none_low_lt(lhs, rhs)


def none_low_gt(lhs, rhs):
    """Greater-than comparison.  None is less than any value."""
    return lhs != rhs and not none_low_lt(lhs, rhs)


def none_low_ge(lhs, rhs):
    """Greater-than-or-equal comparison.  None is less than any value."""
    return lhs == rhs or none_low_gt(lhs, rhs)


def none_low_min(lhs, rhs):
    """Minimum function where None is less than any value."""
    if lhs == None or rhs == None:
        return None
    else:
        return min(lhs, rhs)


def none_high_lt(lhs, rhs):
    """Less-than comparison.  None is greater than any value."""
    return lhs != rhs and (rhs == None or (lhs != None and lhs < rhs))


def none_high_le(lhs, rhs):
    """Less-than-or-equal comparison.  None is greater than any value."""
    return lhs == rhs or none_high_lt(lhs, rhs)


def none_high_gt(lhs, rhs):
    """Greater-than comparison.  None is greater than any value."""
    return lhs != rhs and not none_high_lt(lhs, rhs)


def none_high_ge(lhs, rhs):
    """Greater-than-or-equal comparison.  None is greater than any value."""
    return lhs == rhs or none_high_gt(lhs, rhs)


def none_high_max(lhs, rhs):
    """Maximum function where None is greater than any value."""
    if lhs == None or rhs == None:
        return None
    else:
        return max(lhs, rhs)

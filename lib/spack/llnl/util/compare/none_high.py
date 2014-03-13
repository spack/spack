##############################################################################
# Copyright (c) 2013, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Written by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://scalability-llnl.github.io/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License (as published by
# the Free Software Foundation) version 2.1 dated February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
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

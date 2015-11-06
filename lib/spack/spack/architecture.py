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
import os
import re
import platform

from llnl.util.lang import memoized

import spack
import spack.error as serr


class InvalidSysTypeError(serr.SpackError):
    def __init__(self, sys_type):
        super(InvalidSysTypeError, self).__init__(
            "Invalid sys_type value for Spack: " + sys_type)


class NoSysTypeError(serr.SpackError):
    def __init__(self):
        super(NoSysTypeError, self).__init__(
            "Could not determine sys_type for this machine.")


def get_sys_type_from_spack_globals():
    """Return the SYS_TYPE from spack globals, or None if it isn't set."""
    if not hasattr(spack, "sys_type"):
        return None
    elif hasattr(spack.sys_type, "__call__"):
        return spack.sys_type()
    else:
        return spack.sys_type


def get_sys_type_from_environment():
    """Return $SYS_TYPE or None if it's not defined."""
    return os.environ.get('SYS_TYPE')


def get_sys_type_from_platform():
    """Return the architecture from Python's platform module."""
    sys_type = platform.system() + '-' + platform.machine()
    sys_type = re.sub(r'[^\w-]', '_', sys_type)
    return sys_type.lower()


@memoized
def sys_type():
    """Returns a SysType for the current machine."""
    methods = [get_sys_type_from_spack_globals,
               get_sys_type_from_environment,
               get_sys_type_from_platform]

    # search for a method that doesn't return None
    sys_type = None
    for method in methods:
        sys_type = method()
        if sys_type: break

    # Couldn't determine the sys_type for this machine.
    if sys_type is None:
        return "unknown_arch"

    if not isinstance(sys_type, basestring):
        raise InvalidSysTypeError(sys_type)

    return sys_type

##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from __future__ import print_function

import os
import sys

import llnl.util.tty as tty
import spack
import inspect


class SpackError(Exception):
    """This is the superclass for all Spack errors.
       Subclasses can be found in the modules they have to do with.
    """

    def __init__(self, message, long_message=None):
        super(SpackError, self).__init__()
        self.message = message
        self._long_message = long_message

        # for exceptions raised from child build processes, we save the
        # traceback as a string and print it in the parent.
        self.traceback = None

    @property
    def long_message(self):
        return self._long_message

    def die(self):
        # basic debug message
        tty.error(self.message)
        if self.long_message:
            print(self.long_message)

        # stack trace, etc. in debug mode.
        if spack.debug:
            if self.traceback:
                # exception came from a build child, already got
                # traceback in child, so print it.
                sys.stderr.write(self.traceback)
            else:
                # run parent exception hook.
                sys.excepthook(*sys.exc_info())

        os._exit(1)

    def __str__(self):
        msg = self.message
        if self._long_message:
            msg += "\n    %s" % self._long_message
        return msg

    def __repr__(self):
        args = [repr(self.message), repr(self.long_message)]
        args = ','.join(args)
        qualified_name = inspect.getmodule(
            self).__name__ + '.' + type(self).__name__
        return qualified_name + '(' + args + ')'

    def __reduce__(self):
        return type(self), (self.message, self.long_message)


class UnsupportedPlatformError(SpackError):
    """Raised by packages when a platform is not supported"""

    def __init__(self, message):
        super(UnsupportedPlatformError, self).__init__(message)


class NoNetworkConnectionError(SpackError):
    """Raised when an operation needs an internet connection."""

    def __init__(self, message, url):
        super(NoNetworkConnectionError, self).__init__(
            "No network connection: " + str(message),
            "URL was: " + str(url))
        self.url = url

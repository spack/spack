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

class SpackError(Exception):
    """This is the superclass for all Spack errors.
       Subclasses can be found in the modules they have to do with.
    """
    def __init__(self, message, long_message=None):
        super(SpackError, self).__init__(message)
        self.long_message = long_message


class UnsupportedPlatformError(SpackError):
    """Raised by packages when a platform is not supported"""
    def __init__(self, message):
        super(UnsupportedPlatformError, self).__init__(message)


class NoNetworkConnectionError(SpackError):
    """Raised when an operation needs an internet connection."""
    def __init__(self, message, url):
        super(NoNetworkConnectionError, self).__init__(message)
        self.url = url

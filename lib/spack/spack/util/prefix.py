##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
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
"""
This file contains utilities for managing the installation prefix of a package.
"""
import os


class Prefix(str):
    """This class represents an installation prefix, but provides useful
    attributes for referring to directories inside the prefix.

    Attributes of this object are created on the fly when you request them,
    so any of the following is valid:

    >>> prefix = Prefix('/usr')
    >>> prefix.bin
    /usr/bin
    >>> prefix.lib64
    /usr/lib64
    >>> prefix.share.man
    /usr/share/man
    >>> prefix.foo.bar.baz
    /usr/foo/bar/baz

    Prefix objects behave identically to strings. In fact, they
    subclass ``str``. So operators like ``+`` are legal::

        print('foobar ' + prefix)

    This prints ``foobar /usr``. All of this is meant to make custom
    installs easy.
    """
    def __getattr__(self, attr):
        return Prefix(os.path.join(self, attr))

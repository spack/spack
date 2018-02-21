##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
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
from spack import *
import sys
import os


class Libunwind(AutotoolsPackage):
    """A portable and efficient C programming interface (API) to determine
       the call-chain of a program."""
    homepage = "http://www.nongnu.org/libunwind/"
    url      = "http://download.savannah.gnu.org/releases/libunwind/libunwind-1.1.tar.gz"

    version('1.1', 'fb4ea2f6fbbe45bf032cd36e586883ce')

    # On Darwin, libunwind is available without any additional include paths
    # and libraries - this is because the header is in /usr/include and there
    # is no need to add '-lunwind' since libc.dylib (and libc++.dylib) are
    # already linked with /usr/lib/system/libunwind.dylib. In order to support
    # this case, we allow configuring libunwind as an extrnal library with a
    # prefix that does not exist.

    @property
    def headers(self):
        if sys.platform == 'darwin' and not os.access(self.prefix, os.F_OK):
            return HeaderList([])
        return HeaderList(find(self.prefix.include, 'libunwind.h',
                               recursive=False)) or None

    @property
    def libs(self):
        if sys.platform == 'darwin' and not os.access(self.prefix, os.F_OK):
            return LibraryList([])
        return find_libraries('libunwind', root=self.prefix.lib,
                              shared=('+shared' in self.spec),
                              recursive=False) or None

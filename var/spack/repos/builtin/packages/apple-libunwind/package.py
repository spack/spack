##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
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


class AppleLibunwind(Package):
    """Placeholder package for Apple's analogue to non-GNU libunwind"""

    homepage = "https://opensource.apple.com/source/libunwind/libunwind-35.3/"

    provides('unwind')

    # The 'conflicts' directive only accepts valid spack specs;
    # platforms cannot be negated -- 'platform!=darwin' is not a valid
    # spec -- so expressing a conflict for any platform that isn't
    # Darwin must be expressed by listing a conflict with every
    # platform that isn't Darwin/macOS
    conflicts('platform=linux')
    conflicts('platform=bgq')
    conflicts('platform=cray')

    # Override the fetcher method to throw a useful error message;
    # avoids GitHub issue (#7061) in which the opengl placeholder
    # package threw a generic, uninformative error during the `fetch`
    # step,
    @property
    def fetcher(self):
        msg = """This package is intended to be a placeholder for Apple's
        system-provided, non-GNU-compatible libunwind library.

        Add to your packages.yaml:

        packages:
          apple-libunwind:
            paths:
              apple-libunwind@35.3: /usr
            buildable: False

        """
        raise InstallError(msg)

    def install(self, spec, prefix):
        pass

    @property
    def libs(self):
        """ Export the Apple libunwind library
        """
        libs = find_libraries('libunwind',
                              join_path(self.prefix.lib, 'system'),
                              shared=True, recursive=False)
        if libs:
            return libs
        return None

    @property
    def headers(self):
        """ Export the Apple libunwind header
        """
        hdrs = HeaderList(find(self.prefix.include, 'libunwind.h',
                               recursive=False))
        return hdrs or None

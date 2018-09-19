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


class BuildError(Package):
    """This package has an install method that fails in a build script."""

    homepage = "http://www.example.com/trivial_install"
    url      = "http://www.unit-test-should-replace-this-url/trivial_install-1.0.tar.gz"

    version('1.0', 'foobarbaz')

    def install(self, spec, prefix):
        with open('configure', 'w') as f:
            f.write("""#!/bin/sh\n
echo 'checking build system type... x86_64-apple-darwin16.6.0'
echo 'checking host system type... x86_64-apple-darwin16.6.0'
echo 'checking for gcc... /Users/gamblin2/src/spack/lib/spack/env/clang/clang'
echo 'checking whether the C compiler works... yes'
echo 'checking for C compiler default output file name... a.out'
echo 'checking for suffix of executables...'
echo 'configure: error: in /path/to/some/file:'
echo 'configure: error: cannot run C compiled programs.'
exit 1
""")
        configure()

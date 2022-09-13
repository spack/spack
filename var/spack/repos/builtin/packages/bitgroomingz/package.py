# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install bitgroomingz
#
# You can edit this file again by typing:
#
#     spack edit bitgroomingz
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class Bitgroomingz(CMakePackage):
    """BGZ: Bit Grooming Compressor"""

    homepage = "https://github.com/disheng222/BitGroomingZ"
    git      = "https://github.com/robertu94/BitGroomingZ"

    version('master', branch='master')

    variant('shared', default=True, description='build shared libs')

    # FIXME: Add dependencies if required.
    depends_on('zlib')

    def cmake_args(self):
        args = []
        if "+shared" in self.spec:
            args.append("-DBUILD_SHARED_LIBS=ON")
        else:
            args.append("-DBUILD_SHARED_LIBS=OFF")
        return args


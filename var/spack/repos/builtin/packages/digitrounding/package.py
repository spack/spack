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
#     spack install digitrounding
#
# You can edit this file again by typing:
#
#     spack edit digitrounding
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class Digitrounding(CMakePackage):
    """Standalone version of Digit rounding compressor"""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://github.com/disheng222/digitroundingZ"
    git      = "https://github.com/disheng222/digitroundingZ"


    # FIXME: Add proper versions here.
    version('master', branch="master")
    version('2020-27-20', commit="7b18679aded7a85e6f221f7f5cd4f080f322bc33")

    # FIXME: Add dependencies if required.
    depends_on('zlib')

    variant("shared", default=True, description="build shared libraries")

    def cmake_args(self):
        args = []
        if "+shared" in self.spec:
            args.append("-DBUILD_SHARED_LIBS=ON")
        else:
            args.append("-DBUILD_SHARED_LIBS=OFF")
        return args

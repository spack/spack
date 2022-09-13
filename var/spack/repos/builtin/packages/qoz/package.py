# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
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
#     spack install qoz
#
# You can edit this file again by typing:
#
#     spack edit qoz
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class Qoz(CMakePackage):
    """Quality optimized version of SZ3 is the next generation of the SZ compressor framework"""

    git      = "https://github.com/robertu94/QoZ"
    homepage = git

    version('master', branch='develop')

    maintainers = ['disheng222']

    depends_on('zstd')
    depends_on('gsl')
    depends_on('pkgconfig')


    def cmake_args(self):
        args = [
            "-DQoZ_USE_BUNDLED_ZSTD=OFF",
            "-DQoZ_DEBUG_TIMINGS=OFF",
        ]
        return args

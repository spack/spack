# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
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
#     spack install arc
#
# You can edit this file again by typing:
#
#     spack edit arc
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class Arc(CMakePackage):
    """ARC is an automatic resiliency library designed to provide security to lossy compressed data or other uint8_t data arrays"""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://github.com/FTHPC/ARC"
    url      = "https://github.com/FTHPC/ARC"
    git      = "https://github.com/robertu94/ARC"

    maintainers = ['robertu94']

    version('master', branch='master')

    depends_on('libpressio+sz+zfp', when="+examples")

    variant('examples', description="build examples", default=False)
    variant('shared', description="build shared libraries", default=True)


    def cmake_args(self):
        args = [
            self.define('BUILD_TESTING', self.run_tests),
            self.define_from_variant('BUILD_SHARED_LIBS', 'shared'),
            self.define_from_variant('BUILD_EXAMPLES', 'examples')
        ]
        return args

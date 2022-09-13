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
#     spack install mgardx
#
# You can edit this file again by typing:
#
#     spack edit mgardx
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class Mgardx(CMakePackage):
    """MGARD implementation for research purposes"""

    # FIXME: Add a proper url for your package's homepage here.
    homepage      = "https://github.com/lxAltria/MGARDx"
    git           = "https://github.com/robertu94/MGARDx"

    variant('shared', description="build shared libraries", default=True)

    version('2022-01-27', commit='aabe9de1a331eaeb8eec41125dd45e30c1d03af4')

    depends_on('sz-cpp')
    depends_on('pkgconfig')
    depends_on('zstd')

    def cmake_args(self):
        args = [
            self.define('BUILD_TESTING', self.run_tests),
            self.define_from_variant('BUILD_SHARED_LIBS', 'shared')
        ]
        return args

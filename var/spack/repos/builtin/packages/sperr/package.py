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
#     spack install sperr
#
# You can edit this file again by typing:
#
#     spack edit sperr
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class Sperr(CMakePackage):
    """SPERR is a lossy scientific (floating-point) data compressor that can perform either error-bounded or size-bounded data compression"""

    homepage = "https://github.com/shaomeng/SPERR"
    git      = "https://github.com/robertu94/SPERR"

    version('2022.07.18', commit="640305d049db9e9651ebdd773e6936e2c028ff3a")
    version('2022.05.26', commit="7894a5fe1b5ca5a4aaa952d1779dfc31fd741243")

    depends_on('git', type='build')
    depends_on('zstd', type=('build','link'), when="+zstd")
    depends_on('pkgconf', type=('build'), when="+zstd")

    variant('shared', description="build shared libaries", default=True)
    variant('qz', description="coding terminates by quantization level", default=True)
    variant('zstd', description="use Zstd for more compression", default=True)

    def cmake_args(self):
        args = [
            self.define_from_variant('BUILD_SHARED_LIBS',  'shared'),
            self.define_from_variant('QZ_TERM',  'qz'),
            self.define_from_variant('USE_ZSTD',  'zstd'),
            "-DSPERR_PREFER_RPATH=OFF",
            "-DUSE_BUNDLED_ZSTD=OFF",
            "-DBUILD_CLI_UTILITIES=OFF",
            "-DBUILD_UNIT_TESTS=OFF",
        ]
        return args

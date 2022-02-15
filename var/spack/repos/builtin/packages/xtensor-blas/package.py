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
#     spack install xtensor-blas
#
# You can edit this file again by typing:
#
#     spack edit xtensor-blas
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class XtensorBlas(CMakePackage):
    """xtensor-blas"""

    homepage = "https://xtensor-stack.github.io"
    url      = "https://github.com/xtensor-stack/xtensor-blas/archive/refs/tags/1.0.0.tar.gz"
    git = "git://github.com/xtensor-stack/xtensor-blas.git"

    version('develop', branch='master')
    version('0.20.0', sha256='272f5d99bb7511a616bfe41b13a000e63de46420f0b32a25fa4fb935b462c7ff')
    version('0.19.2', sha256='ef678c0e3f581cc8d61ea002c904c76513c8b0f798f9c9acaf980a835f9d09aa')
    version('0.19.1', sha256='c77cc4e2297ebd22d0d1c6e8d0a6cf0975176afa8cb99dbfd5fb2be625a0248f')
    version('0.19.0', sha256='0fa8001afa2d9f7fb1d3c101ae04565f39ef2880a84acec216e699ed14950cb4')

    depends_on('cmake@3.1:', type='build')
    depends_on('xtensor@0.24.0:', when='@0.20:')
    depends_on('xtensor', when='@:0.20')

    # C++14 support
    conflicts('%gcc@:4.8')
    conflicts('%clang@:3.5')

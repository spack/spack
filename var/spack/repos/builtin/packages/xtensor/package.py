# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Xtensor(CMakePackage):
    """Multi-dimensional arrays with broadcasting and lazy computing"""

    homepage = "http://quantstack.net/xtensor"
    url      = "https://github.com/QuantStack/xtensor/archive/0.13.1.tar.gz"
    git      = "https://github.com/QuantStack/xtensor.git"

    maintainers = ['ax3l']

    version('develop', branch='master')
    version('0.15.1', 'c24ecc406003bd1ac22291f1f7cac29a')
    version('0.13.1', '80e7e33f05066d17552bf0f8b582dcc5')

    variant('xsimd', default=True,
            description='Enable SIMD intrinsics')

    depends_on('xtl')
    depends_on('xtl@0.4.0:0.4.99', when='@0.15.1:')
    depends_on('xtl@0.3.3:0.3.99', when='@0.13.1')
    depends_on('xsimd@4.0.0', when='@0.15.1 +xsimd')
    depends_on('xsimd@3.1.0', when='@0.13.1 +xsimd')

    # C++14 support
    conflicts('%gcc@:4.8')
    conflicts('%clang@:3.5')
    # untested: conflicts('%intel@:15')
    # untested: conflicts('%pgi@:14')

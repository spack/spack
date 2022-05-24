# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Ecbuild(CMakePackage):
    """ecBuild is the ECMWF build system. It is built on top of CMake and
    consists of a set of macros as well as a wrapper around CMake"""

    homepage = 'https://github.com/ecmwf/ecbuild'
    url = 'https://github.com/ecmwf/ecbuild/archive/refs/tags/3.6.1.tar.gz'

    maintainers = ['skosukhin']

    version('3.6.5', sha256='98bff3d3c269f973f4bfbe29b4de834cd1d43f15b1c8d1941ee2bfe15e3d4f7f')
    version('3.6.1', sha256='796ccceeb7af01938c2f74eab0724b228e9bf1978e32484aa3e227510f69ac59')

    depends_on('cmake@3.11:', type=('build', 'run'))

    # See https://github.com/ecmwf/ecbuild/issues/35
    depends_on('cmake@:3.19', type=('build', 'run'), when='@:3.6.1')

    # Some of the installed scripts require running Perl:
    depends_on('perl', type=('build', 'run'))

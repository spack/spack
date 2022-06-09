# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Ecbuild(CMakePackage):
    """ecBuild is the ECMWF build system. It is built on top of CMake and
    consists of a set of macros as well as a wrapper around CMake,"""

    homepage = 'https://github.com/ecmwf/ecbuild'
    url = 'https://github.com/ecmwf/ecbuild/archive/refs/tags/3.6.1.tar.gz'

    maintainers = ['skosukhin']

    version('3.6.1', sha256='796ccceeb7af01938c2f74eab0724b228e9bf1978e32484aa3e227510f69ac59')

    # Some of the tests (ECBUILD-415 and test_ecbuild_regex_escape) fail with
    # cmake@2.20.0 and it is not yet clear why. For now, we simply limit the
    # version of cmake to the latest '3.19.x':
    depends_on('cmake@3.11:3.19', type=('build', 'run'))

    # Some of the installed scripts require running Perl:
    depends_on('perl', type=('build', 'run'))

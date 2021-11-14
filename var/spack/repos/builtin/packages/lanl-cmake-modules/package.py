# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class LanlCmakeModules(CMakePackage):
    '''CMake modules for projects that have not yet adopted modern CMake.
    '''

    maintainers = ['tuxfan']
    homepage = 'https://tuxfan.github.io/lanl-cmake-modules'
    git      = 'https://github.com/tuxfan/lanl-cmake-modules.git'

    version('develop', branch='develop')

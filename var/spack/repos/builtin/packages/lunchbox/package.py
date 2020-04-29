# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Lunchbox(CMakePackage):
    """A core C++ library for multi-threaded programming."""

    homepage = "https://github.com/Eyescale/Lunchbox"
    git = "https://github.com/Eyescale/Lunchbox.git"
    generator = 'Ninja'

    version('develop', submodules=True)
    version('1.17', tag='1.17.0', preferred=True, submodules=True)

    depends_on('cmake@3.1:', type='build')
    depends_on('ninja', type='build')

    depends_on('boost')
    depends_on('servus')

    patch('fix_hwloc_2.0.patch')

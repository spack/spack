# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Vmmlib(CMakePackage):
    """A templatized C++ vector and matrix math library"""

    homepage = "https://github.com/Eyescale/vmmlib"
    git = "https://github.com/Eyescale/vmmlib.git"
    generator = 'Ninja'

    version('develop', branch='master')
    version('1.14.0', tag='1.14.0', submodules=True, preferred=True)

    depends_on('cmake@3.1:', type='build')
    depends_on('ninja', type='build')
    depends_on('boost', type='build')

    patch('fix_implicit_copy_constructor.patch')

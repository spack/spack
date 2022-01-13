# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Servus(CMakePackage):
    """Servus is a small C++ network utility library that provides a zeroconf
       API, URI parsing and UUIDs."""

    homepage = "https://github.com/HBPVIS/Servus"
    git = "https://github.com/HBPVIS/Servus.git"
    generator = 'Ninja'

    version('develop', submodules=True)
    version('1.5.2', tag='1.5.2', submodules=True, preferred=True)

    depends_on('cmake@3.1:', type='build')
    depends_on('ninja', type='build')
    depends_on('boost', type='build')

    patch('fix_uint128_t_class.patch', when='@1.5.2:')
    patch('missing-include.diff')

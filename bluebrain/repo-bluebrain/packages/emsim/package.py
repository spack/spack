# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Emsim(CMakePackage):
    """ EMSim is a tool for computing VSD and LFP """

    homepage = "https://github.com/BlueBrain/EMSim"
    git = "https://github.com/BlueBrain/EMSim"

    generator = 'Ninja'

    version('develop')
    version('1.0.1', tag='v1.0.1')

    depends_on('cmake@3.1:', type='build')
    depends_on('ninja', type='build')
    depends_on('brion@3.3.3:3.999')
    depends_on('ispc', type='build')
    depends_on('boost +shared')

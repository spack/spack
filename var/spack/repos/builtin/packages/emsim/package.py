# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Emsim(CMakePackage):
    """ EMSim is a tool for computing VSD and LFP """

    git = "ssh://bbpcode.epfl.ch/viz/EMSim"

    generator = 'Ninja'

    version('1.0.0', tag='v1.0.0', submodules=True)

    depends_on('cmake@3.1:', type='build')
    depends_on('ninja', type='build')
    depends_on('brion +python')
    # Eyescale cmake requires Python (!)
    depends_on('python@3.6:', type='build')

    patch('cmake.patch')

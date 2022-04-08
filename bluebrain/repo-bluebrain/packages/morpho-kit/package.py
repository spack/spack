# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class MorphoKit(CMakePackage):
    """Higher-level library for reading / writing morphology files"""

    homepage = "https://bbpgitlab.epfl.ch/hpc/morpho-kit"
    git      = "git@bbpgitlab.epfl.ch:hpc/morpho-kit.git"

    version('develop', branch='main', submodules=True, get_full_repo=True)
    version('0.3.3', tag='0.3.3', submodules=True, get_full_repo=True)
    version('0.3.2', tag='v0.3.2', submodules=True, get_full_repo=True)
    version('0.3.1', tag='v0.3.1', submodules=True, get_full_repo=True)
    version('0.3.0', tag='v0.3.0', submodules=True, get_full_repo=True)
    version('0.2.0', tag='v0.2.0', submodules=True, get_full_repo=True)

    depends_on('cmake@3.2:', type='build')
    depends_on('morphio@2.3.9:')
    depends_on('cli11', when='@0.3.3:')      # for utilities
    depends_on('libsonata', when='@0.3.3:')  # for utilities
    depends_on('highfive@2.4.0:', when='@0.3.3:')  # for utilities

    depends_on('boost', when='@0.2.0')

    patch('h5.patch', when='@0.3.2')

    def cmake_args(self):
        return [
            '-DBUILD_BINDINGS:BOOL=OFF',
        ]

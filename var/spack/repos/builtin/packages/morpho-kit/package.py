# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class MorphoKit(CMakePackage):
    """Higher-level library for reading / writing morphology files"""

    homepage = "https://bbpcode.epfl.ch/code/#/projects/nse/morpho-kit,dashboards/default"
    url      = "https://bbpcode.epfl.ch/code/a/nse/morpho-kit"
    git      = "ssh://bbpcode.epfl.ch/nse/morpho-kit"

    version('develop', branch='master', submodules=True, get_full_repo=True)
    version('0.2.0', tag='v0.2.0', submodules=True, get_full_repo=True)
    version('0.1.0', tag='v0.1.0', submodules=True, get_full_repo=True)

    depends_on('cmake@3.2:', type='build')
    depends_on('morphio', when='@0.1.1:')
    depends_on('morphio@:2.2.1', when='@0.1.0')
    depends_on('morphio@2.3.9:', when='@0.2.0:')
    depends_on('boost', when='@0.2.0:')

    def cmake_args(self):
        return [
            '-DBUILD_BINDINGS:BOOL=OFF',
        ]

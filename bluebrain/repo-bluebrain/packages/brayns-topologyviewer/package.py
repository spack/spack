# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class BraynsTopologyviewer(CMakePackage):
    """Brayns use-case plugin for interactive visualization of
       the topology of neuron simulation data"""

    homepage = "https://bbpgitlab.epfl.ch/viz/archive/Gerrit/Brayns-UC-TopologyViewer"
    git = "git@bbpgitlab.epfl.ch:viz/archive/Gerrit/Brayns-UC-TopologyViewer.git"

    generator = 'Ninja'

    version('develop', submodules=True)
    version('0.1.0', tag='v0.1.0', submodules=True)

    depends_on('cmake@3.1:', type='build')
    depends_on('ninja', type='build')
    depends_on('brayns')
    depends_on('highfive@2.1: +boost ~mpi')

    def patch(self):
        if self.spec.satisfies('%gcc@9:'):
            filter_file(
                r'-Werror',
                '-Werror -Wno-error=pessimizing-move',
                'CMake/common/CommonCompiler.cmake'
            )

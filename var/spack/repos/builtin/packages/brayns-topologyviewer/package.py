# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class BraynsTopologyviewer(CMakePackage):
    """Brayns use-case plugin for interactive visualization of
       the topology of neuron simulation data"""

    git = "ssh://bbpcode.epfl.ch/viz/Brayns-UC-TopologyViewer.git"

    generator = 'Ninja'

    version('develop', submodules=True)
    version('0.1.0', tag='v0.1.0', submodules=True)

    depends_on('cmake@3.1:', type='build')
    depends_on('ninja', type='build')
    depends_on('brayns')
    depends_on('highfive@2.1: +boost ~mpi')

# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PlacementAlgorithm(PythonPackage):
    """Morphology placement algorithm"""

    homepage = "https://bbpgitlab.epfl.ch/nse/placement-algorithm/"
    git      = "git@bbpgitlab.epfl.ch:nse/placement-algorithm.git"

    version('develop', branch='master')
    version('2.2.0', tag='placement-algorithm-v2.2.0')
    version('2.1.4', tag='placement-algorithm-v2.1.4')

    build_directory = 'python'

    depends_on('py-setuptools', type=('build', 'run'))

    depends_on('py-lxml@4.0:', type='run')
    depends_on('py-numpy@1.8:', type='run')
    depends_on('py-pandas@0.19:', type='run')
    depends_on('py-six', type='run')

    depends_on('py-morphio@3.0:3.999', type='run')
    depends_on('py-morph-tool@2.9.0:', type='run', when='@2.2.0:')
    depends_on('py-morph-tool@0.1.3:2.8.99', type='run', when='@:2.1.99')
    depends_on('py-neurom@3.0:3.999', type='run', when='@2.2.0:')
    depends_on('py-neurom@2.0:2.99', type='run', when='@:2.1.99')
    depends_on('py-neuroc@:0.2.7', type='run', when='@:2.1.99')
    depends_on('py-neuroc@0.2.8:0.999', type='run', when='@2.2.0:')
    depends_on('py-mpi4py@3.0.3:', type='run')
    depends_on('py-tqdm@4.0:', type='run')
    depends_on('py-voxcell@2.7:3.99', type='run')
    depends_on('py-dask+distributed+bag', type='run')

    depends_on('py-region-grower@0.1.5:0.1.99', type='run', when='@:2.1.99')

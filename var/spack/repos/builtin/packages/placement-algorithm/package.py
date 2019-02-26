# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PlacementAlgorithm(PythonPackage):
    """Morphology placement algorithm"""

    homepage = "https://bbpcode.epfl.ch/code/#/admin/projects/building/placementAlgorithm"
    git      = "ssh://bbpcode.epfl.ch/building/placementAlgorithm"

    version('develop', branch='master')
    version('2.0.6', tag='placement-algorithm-v2.0.6', preferred=True)

    build_directory = 'python'

    depends_on('py-setuptools', type=('build','run'))

    depends_on('py-lxml', type='run')
    depends_on('py-numpy', type='run')
    depends_on('py-pandas', type='run')
    depends_on('py-six', type='run')

    depends_on('py-morphio@2.0:', type='run')
    depends_on('py-morph-tool@0.1.3:', type='run')
    depends_on('py-mpi4py@2.0:2.99', type='run')
    depends_on('py-tqdm@4.0:', type='run')
    depends_on('py-voxcell@2.5:', type='run')

    depends_on('py-region-grower@0.1.0:', type='run')

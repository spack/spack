# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PlacementAlgorithm(PythonPackage):
    """Morphology placement algorithm"""

    homepage = "https://bbpgitlab.epfl.ch/nse/placement-algorithm/"
    git      = "git@bbpgitlab.epfl.ch:nse/placement-algorithm.git"

    version('develop')
    version('2.3.0', tag='placement-algorithm-v2.3.0')

    build_directory = 'python'

    depends_on('python@3.6:', type=('build', 'run'))
    depends_on('py-setuptools', type=('build', 'run'))

    depends_on('py-jsonschema@3.2.0:', type=('build', 'run'))
    depends_on('py-lxml@4.0:', type=('build', 'run'))
    depends_on('py-numpy@1.8:', type=('build', 'run'))
    depends_on('py-pandas@0.19:', type=('build', 'run'))
    depends_on('py-scipy@1.2.0:', type=('build', 'run'))
    depends_on('py-pyyaml@5.3.1:', type=('build', 'run'))

    depends_on('py-morphio@3.0:', type=('build', 'run'))
    depends_on('py-morph-tool@2.9.0:2.999', type=('build', 'run'))
    depends_on('py-mpi4py@3.0.3:', type=('build', 'run'))
    depends_on('py-tqdm@4.0:', type=('build', 'run'))
    depends_on('py-voxcell@2.7:3.99', type=('build', 'run'))
    depends_on('py-dask+distributed+bag@2.15:', type=('build', 'run'))

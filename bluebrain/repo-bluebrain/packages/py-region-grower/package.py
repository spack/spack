# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyRegionGrower(PythonPackage):
    """Python library for space-aware neuron synthesis"""

    homepage = "https://bbpgitlab.epfl.ch/neuromath/region-grower"
    git      = "git@bbpgitlab.epfl.ch:neuromath/region-grower.git"

    version('develop', branch='main')
    version('0.3.0', tag='region-grower-v0.3.0')

    depends_on('py-setuptools', type='build')

    depends_on('py-attrs@19.3.0:', type=('build', 'run'))
    depends_on('py-click@7.0:', type=('build', 'run'))
    depends_on('py-dask+dataframe+distributed@2.15.0:2021.8.0,2021.9.0:', type=('build', 'run'))
    depends_on('py-diameter-synthesis@0.2.5:0.999', type=('build', 'run'))
    depends_on('py-morphio@3.0:3.999', type=('build', 'run'))
    depends_on('py-morph-tool@2.9.0:2.999', type=('build', 'run'))
    depends_on('py-neuroc@0.2.8:0.999', type=('build', 'run'))
    depends_on('py-neurom@3.0:3.999', type=('build', 'run'))
    depends_on('py-tns@2.5.0:2.999', type=('build', 'run'))
    depends_on('py-tqdm@4.28.1:', type=('build', 'run'))
    depends_on('py-voxcell@2.7:3.999', type=('build', 'run'))
    depends_on('py-dask-mpi@2.0.0:', type=('build', 'run'))
    depends_on('py-mpi4py@3.0.3:', type=('build', 'run'))

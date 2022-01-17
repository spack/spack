# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyVoxcell(PythonPackage):
    """Python library for handling volumetric data"""

    homepage = "https://bbpgitlab.epfl.ch/nse/voxcell"
    git      = "git@bbpgitlab.epfl.ch:nse/voxcell.git"

    version('develop', branch='main')
    version('3.1.0', tag='voxcell-v3.1.0')
    version('2.7.4', tag='voxcell-v2.7.4')

    depends_on('py-setuptools', type='build')

    depends_on('py-six@1.0:', type=('build', 'run'), when='@:2.999')
    depends_on('py-future@0.16:', type=('build', 'run'), when='@:2.999')
    depends_on('py-h5py@2.3:2.999', type=('build', 'run'), when='@:2.999')
    depends_on('py-h5py@3.1.0:', type=('build', 'run'), when='@3.0.0:')
    depends_on('py-numpy@1.9:', type=('build', 'run'))
    depends_on('py-pandas@0.24.2:', type=('build', 'run'))
    depends_on('py-pynrrd@0.4.0:', type=('build', 'run'))
    depends_on('py-requests@2.18:', type=('build', 'run'))
    depends_on('py-scipy@1.2.0:', type=('build', 'run'))

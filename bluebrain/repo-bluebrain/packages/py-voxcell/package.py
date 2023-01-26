# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyVoxcell(PythonPackage):
    """Python library for handling volumetric data"""

    homepage = "https://github.com/BlueBrain/voxcell"
    git = "https://github.com/BlueBrain/voxcell.git"
    pypi = "voxcell/voxcell-3.1.2.tar.gz"

    version('develop', branch='main')
    version('3.1.3', sha256='1e5453777dd9df5e424f05ba71ed470e66489bf0902ecb997e9a5d825cd21a46')
    version('3.1.2', sha256='d3d4dc3ebc95662502db2fa7fab33bbc84eca323f5ce1104b9668f7ae0d29eaa')
    version('2.7.4', tag='voxcell-v2.7.4')

    depends_on('py-setuptools', type='build')
    depends_on('py-setuptools-scm', type='build')

    depends_on('py-six@1.0:', type=('build', 'run'), when='@:2')
    depends_on('py-future@0.16:', type=('build', 'run'), when='@:2')
    depends_on('py-h5py@2.3:2', type=('build', 'run'), when='@:2')
    depends_on('py-h5py@3.1.0:', type=('build', 'run'), when='@3:')
    depends_on('py-numpy@1.9:', type=('build', 'run'))
    depends_on('py-pandas@0.24.2:', type=('build', 'run'))
    depends_on('py-pynrrd@0.4.0:', type=('build', 'run'))
    depends_on('py-requests@2.18:', type=('build', 'run'))
    depends_on('py-scipy@1.2.0:', type=('build', 'run'))

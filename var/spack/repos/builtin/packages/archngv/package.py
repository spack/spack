# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Archngv(PythonPackage):
    """NGV builder"""

    homepage = "https://bbpcode.epfl.ch/code/#/admin/projects/molecularsystems/ArchNGV"
    git      = "ssh://bbpcode.epfl.ch/molecularsystems/ArchNGV"

    version('develop', branch='master')
    version('0.0.0', tag='archngv-v0.0.0', preferred=True)

    depends_on('python@3.6:', type=('build', 'run'))
    depends_on('py-setuptools', type=('build', 'run'))

    depends_on('py-cached-property@1.3:', type='run')
    depends_on('py-click@7.0:7.999', type='run')
    depends_on('py-h5py~mpi@2.3:', type='run')
    depends_on('py-jenkspy@0.1.4:', type='run')
    depends_on('py-numpy@1.13:', type='run')
    depends_on('py-numpy-stl@2.7:', type='run')
    depends_on('py-openmesh@1.1.2:', type='run')
    depends_on('py-pandas@0.17:', type='run')
    depends_on('py-pyyaml@3.0:', type='run')
    depends_on('py-scipy@1.0:', type='run')
    depends_on('py-tess@0.2.2:', type='run')
    depends_on('py-trimesh@2.21.15:', type='run')

    depends_on('py-bluepy@0.13.5:', type='run')
    depends_on('py-morphmath', type='run')
    depends_on('py-morphspatial', type='run')
    depends_on('py-spatial-index', type='run')
    depends_on('py-tmd@2.0.4:', type='run')
    depends_on('py-tns@space2', type='run')
    depends_on('py-voxcell@2.6.0:', type='run')

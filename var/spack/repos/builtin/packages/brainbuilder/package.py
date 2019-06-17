# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Brainbuilder(PythonPackage):
    """Miscellaneous circuit building utilities"""

    homepage = "https://bbpcode.epfl.ch/code/#/admin/projects/nse/brainbuilder"
    git      = "ssh://bbpcode.epfl.ch/nse/brainbuilder"

    version('develop', branch='master')
    version('0.11.3', tag='brainbuilder-v0.11.3')
    version('0.10.5', tag='brainbuilder-v0.10.5')
    version('0.9.2', tag='brainbuilder-v0.9.2')
    version('0.8.1', tag='brainbuilder-v0.8.1')

    depends_on('py-setuptools', type=('build', 'run'))

    depends_on('py-click@7.0:7.999', type='run')
    depends_on('py-future@0.16:', type='run')
    depends_on('py-h5py~mpi@2.6:', type='run')
    depends_on('py-lxml@3.3:', type='run')
    depends_on('py-numpy@1.9:', type='run')
    depends_on('py-pandas@0.17:', type='run')
    depends_on('py-pytables@3.4:', type='run')
    depends_on('py-pyyaml@1.0:', type='run')
    depends_on('py-scipy@0.13:', type='run')
    depends_on('py-six@1.0:', type='run')
    depends_on('py-tqdm@4.0:', type='run')

    depends_on('py-bluepy@0.12.5:', type='run')
    depends_on('py-voxcell@2.6:', type='run')

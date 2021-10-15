# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Brainbuilder(PythonPackage):
    """Miscellaneous circuit building utilities"""

    homepage = "https://bbpgitlab.epfl.ch/nse/brainbuilder/"
    git      = "git@bbpgitlab.epfl.ch:nse/brainbuilder.git"

    version('develop')
    version('0.16.1', tag='brainbuilder-v0.16.1')

    variant('reindex', default=True, description='Install requirements for reindex')

    depends_on('py-setuptools', type=('build', 'run'))

    depends_on('py-click@7.0:7.999', type='run')
    depends_on('py-h5py@3.1.0:', type='run')
    depends_on('py-lxml@3.3:', type='run')
    depends_on('py-numpy@1.9:', type='run')
    depends_on('py-pandas@1.0.0:', type='run')
    depends_on('py-scipy@0.13:', type='run')
    depends_on('py-tqdm@4.0:', type='run')
    depends_on('py-bluepy@2.1:2.999', type='run')
    depends_on('py-libsonata@0.1.6:', type='run')
    depends_on('py-voxcell@3.0.0:', type='run')

    # reindex
    depends_on('py-morphio@3.0.0:3.999', type='run', when='+reindex')

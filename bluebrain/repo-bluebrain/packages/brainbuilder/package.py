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
    version('0.17.0', tag='brainbuilder-v0.17.0')

    depends_on('py-setuptools', type=('build', 'run'))

    depends_on('py-click@7.0:8.999', type=('build', 'run'))
    depends_on('py-h5py@3.1.0:', type=('build', 'run'))
    depends_on('py-jsonschema@3.2.0:', type=('build', 'run'))
    depends_on('py-lxml@3.3:', type=('build', 'run'))
    depends_on('py-numpy@1.9:', type=('build', 'run'))
    depends_on('py-pandas@1.0.0:', type=('build', 'run'))
    depends_on('py-scipy@0.13:', type=('build', 'run'))
    depends_on('py-tqdm@4.0:', type=('build', 'run'))
    depends_on('py-bluepy@2.1:', type=('build', 'run'))
    depends_on('py-libsonata@0.1.6:', type=('build', 'run'))
    depends_on('py-voxcell@3.1.0:', type=('build', 'run'))
    depends_on('py-morphio@3.0.0:3.999', type=('build', 'run'))

    depends_on('py-attrs@:19.999', type=('build', 'run'))
    depends_on('py-entity-management@0.1.11:0.999', type=('build', 'run'))
    depends_on('py-subcellular-querier@0.0.3:', type=('build', 'run'))
    depends_on('py-tables@3.4:', type=('build', 'run'))

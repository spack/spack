# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PySubcellularQuerier(PythonPackage):
    """Query and transform data for subcellular phase in circuit building."""

    homepage = "https://bbpgitlab.epfl.ch/nse/archive/subcellular-querier.git"
    git = "git@bbpgitlab.epfl.ch:nse/archive/subcellular-querier.git"

    version('0.0.3', tag='subcellular-querier-v0.0.3')

    depends_on('py-setuptools', type=('build', 'run'))

    depends_on('py-entity-management@0.1.10:0.999', type=('build', 'run'))
    depends_on('py-tables@3.4.4:', type=('build', 'run'))
    depends_on('py-pandas@0.24.1:', type=('build', 'run'))
    depends_on('py-python-magic@0.4.15:', type=('build', 'run'))
    depends_on('py-pathlib2@2.3.3:', type=('build', 'run'))
    depends_on('py-click@7.0:', type=('build', 'run'))
    depends_on('py-requests@2.21.0:', type=('build', 'run'))

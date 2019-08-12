# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyOpenpmdValidator(PythonPackage):
    """Validator and Example Scripts for the openPMD markup.

    openPMD is an open standard for particle-mesh data files."""

    homepage = "http://www.openPMD.org"
    url      = "https://github.com/openPMD/openPMD-validator/archive/1.0.0.2.tar.gz"
    maintainers = ['ax3l']

    version('1.0.0.2', '2b71b786288c1e7a2134bd6818ad1999')

    depends_on('py-setuptools', type='build')
    depends_on('py-numpy@1.6.1:', type=('build', 'run'))
    depends_on('py-python-dateutil@2.3.0:', type=('build', 'run'))
    depends_on('py-h5py@2.0.0:', type=('build', 'run'))

# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyOpenpmdValidator(PythonPackage):
    """Validator and Example Scripts for the openPMD markup.

    openPMD is an open standard for particle-mesh data files."""

    homepage = "https://www.openPMD.org"
    url      = "https://github.com/openPMD/openPMD-validator/archive/refs/tags/1.1.0.2.tar.gz"
    git      = "https://github.com/openPMD/openPMD-validator.git"

    maintainers = ['ax3l']

    version('1.1.0.2', sha256='b30be7957c2e1e7de67d81fad64492c3a1ecd25db231293d896da116a71ecca5')
    version('1.1.0.1', sha256='93031f50ddeb747ebd6aabca249aa6bf0491d570de56746d7a98d6453427f191')
    version('1.0.0.2', sha256='1b97452991feb0f0ac1ffb3c92b7f9743a86b0b5390dbbfb21160e04f0a35a95')

    depends_on('py-setuptools', type='build')
    depends_on('py-numpy@1.6.1:', type=('build', 'run'))
    depends_on('py-python-dateutil@2.3.0:', type=('build', 'run'))
    depends_on('py-h5py@2.0.0:', type=('build', 'run'))

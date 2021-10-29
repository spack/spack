# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPybids(PythonPackage):
    """bids: interface with datasets conforming to BIDS"""

    homepage = "https://github.com/bids-standard/pybids"
    pypi     = "pybids/pybids-0.13.1.tar.gz"

    version('0.13.2', sha256='9692013af3b86b096b5423b88179c6c9b604baff5a6b6f89ba5f40429feb7a3e')
    version('0.13.1', sha256='c920e1557e1dae8b671625d70cafbdc28437ba2822b2db9da4c2587a7625e3ba')
    version('0.9.5', sha256='0e8f8466067ff3023f53661c390c02702fcd5fe712bdd5bf167ffb0c2b920430')

    depends_on('python@3.5:', when='@0.10:', type=('build', 'run'))
    depends_on('python@2.7:2,3.5:', type=('build', 'run'))
    depends_on('py-setuptools@30.3.0:', type='build')
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-scipy', type=('build', 'run'))
    depends_on('py-nibabel@2.1:', type=('build', 'run'))
    depends_on('py-pandas@0.23:', type=('build', 'run'))
    depends_on('py-patsy', type=('build', 'run'))
    depends_on('py-sqlalchemy@:1.3', when='@0.12.4:', type=('build', 'run'))
    depends_on('py-sqlalchemy', type=('build', 'run'))
    depends_on('py-bids-validator', type=('build', 'run'))
    depends_on('py-num2words', type=('build', 'run'))
    depends_on('py-click', when='@0.12.1:', type=('build', 'run'))

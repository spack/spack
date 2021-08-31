# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPybids(PythonPackage):
    """bids: interface with datasets conforming to BIDS"""

    homepage = "https://github.com/bids-standard/pybids"
    pypi     = "pybids/pybids-0.13.1.tar.gz"

    version('0.13.1', sha256='c920e1557e1dae8b671625d70cafbdc28437ba2822b2db9da4c2587a7625e3ba')

    depends_on('python@3.5:', type=('build', 'run'))
    depends_on('py-setuptools@30.3.0:', type='build')
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-scipy', type=('build', 'run'))
    depends_on('py-nibabel@2.1:', type=('build', 'run'))
    depends_on('py-pandas@0.23:', type=('build', 'run'))
    depends_on('py-patsy', type=('build', 'run'))
    depends_on('py-sqlalchemy@:1.3.999', type=('build', 'run'))
    depends_on('py-bids-validator', type=('build', 'run'))
    depends_on('py-num2words', type=('build', 'run'))
    depends_on('py-click', type=('build', 'run'))

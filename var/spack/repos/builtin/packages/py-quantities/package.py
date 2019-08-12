# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyQuantities(PythonPackage):
    """Support for physical quantities with units, based on numpy"""

    homepage = "http://python-quantities.readthedocs.org"
    url      = "https://pypi.io/packages/source/q/quantities/quantities-0.12.1.tar.gz"

    version('0.12.1', '9c9ecda15e905cccfc420e5341199512')
    version('0.11.1', 'f4c6287bfd2e93322b25a7c1311a0243',
            url="https://pypi.io/packages/source/q/quantities/quantities-0.11.1.zip")

    conflicts('py-numpy@1.13:', when='@:0.11.99')

    depends_on('python@2.6.0:')
    depends_on('py-numpy@1.4.0:', type=('build', 'run'))

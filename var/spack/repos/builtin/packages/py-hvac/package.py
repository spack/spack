# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyHvac(PythonPackage):
    """HashiCorp Vault API client"""

    homepage = "https://github.com/ianunruh/hvac/"
    url      = "https://github.com/ianunruh/hvac/archive/v0.2.17.tar.gz"

    version('0.2.17', '62c42b422ebf336e7499422af4d30003')

    depends_on('py-setuptools', type='build')
    depends_on('py-requests@2.7.0:', type=('build', 'run'))

# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyHttpretty(PythonPackage):
    """HTTP client mock for Python."""

    homepage = "https://httpretty.readthedocs.io/en/latest/"
    pypi     = "httpretty/httpretty-1.1.3.tar.gz"

    version('1.1.3', sha256='229ade39175ea4324e767f29dc24e5f846fbc72bf80e1a919b2547a6574ff601')

    depends_on('python@3:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')

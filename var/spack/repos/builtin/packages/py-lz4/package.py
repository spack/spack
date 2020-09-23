# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyLz4(PythonPackage):
    """lz4 (compression library) bindings for Python"""

    homepage = "https://github.com/python-lz4/python-lz4"
    url      = "https://files.pythonhosted.org/packages/4c/c3/97c5aaeb8c70eafb0cba7dcbcb7709c2697d8a92bdef90d36b018dc502f6/lz4-3.1.0.tar.gz"

    version('3.1.0', sha256='debe75513db3eb9e5cdcd82a329ff38374b6316ab65b848b571e0404746c1e05')

    depends_on('python@3.4:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')

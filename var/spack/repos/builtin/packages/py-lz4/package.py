# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package_defs import *


class PyLz4(PythonPackage):
    """lz4 (compression library) bindings for Python"""

    homepage = "https://github.com/python-lz4/python-lz4"
    pypi = "lz4/lz4-3.1.0.tar.gz"

    version('3.1.3', sha256='081ef0a3b5941cb03127f314229a1c78bd70c9c220bb3f4dd80033e707feaa18')
    version('3.1.0', sha256='debe75513db3eb9e5cdcd82a329ff38374b6316ab65b848b571e0404746c1e05')

    depends_on('python@3.5:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-setuptools-scm', type='build')
    depends_on('py-pkgconfig', type='build')
    depends_on('lz4@1.7.5:')
    depends_on('py-future', when='^python@:2', type=('build', 'run'))

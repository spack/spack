# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyOptEinsum(PythonPackage):
    """Optimized Einsum: A tensor contraction order optimizer."""

    homepage = "https://github.com/dgasmith/opt_einsum"
    url      = "https://pypi.io/packages/source/o/opt_einsum/opt_einsum-3.1.0.tar.gz"

    version('3.1.0', sha256='edfada4b1d0b3b782ace8bc14e80618ff629abf53143e1e6bbf9bd00b11ece77')

    depends_on('python@3.5:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-numpy@1.7:', type=('build', 'run'))
    depends_on('py-pytest', type='test')
    depends_on('py-pytest-cov', type='test')
    depends_on('py-pytest-pep8', type='test')

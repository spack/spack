# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyLazyarray(PythonPackage):
    """a Python package that provides a lazily-evaluated numerical array class,
    larray, based on and compatible with NumPy arrays."""

    homepage = "http://bitbucket.org/apdavison/lazyarray/"
    url      = "https://pypi.io/packages/source/l/lazyarray/lazyarray-0.2.8.tar.gz"

    version('0.2.10', '336033357459e66cbca5543bf003a2ba')
    version('0.2.8',  '8e0072f0892b9fc0516e7048f96e9d74')

    depends_on('py-numpy@1.3:', type=('build', 'run'))
    depends_on('py-numpy@1.5:', type=('build', 'run'), when='^python@3:')

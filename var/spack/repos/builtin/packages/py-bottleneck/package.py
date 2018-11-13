# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyBottleneck(PythonPackage):
    """A collection of fast NumPy array functions written in Cython."""
    homepage = "https://pypi.python.org/pypi/Bottleneck/1.0.0"
    url      = "https://pypi.io/packages/source/B/Bottleneck/Bottleneck-1.0.0.tar.gz"

    version('1.2.1', sha256='6efcde5f830aed64feafca0359b51db0e184c72af8ba6675b4a99f263922eb36')
    version('1.0.0', '380fa6f275bd24f27e7cf0e0d752f5d2')

    depends_on('py-setuptools', type='build')
    depends_on('py-numpy', type=('build', 'run'))

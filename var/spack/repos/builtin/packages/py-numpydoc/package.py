# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyNumpydoc(PythonPackage):
    """numpydoc - Numpy's Sphinx extensions"""

    homepage = "https://github.com/numpy/numpydoc"
    url      = "https://pypi.io/packages/source/n/numpydoc/numpydoc-0.6.0.tar.gz"

    version('0.6.0', '5f1763c44e613850d56ba1b1cf1cb146')

    depends_on('python@2.6:2.8,3.3:')
    depends_on('py-setuptools',    type='build')
    depends_on('py-sphinx@1.0.1:', type='build')

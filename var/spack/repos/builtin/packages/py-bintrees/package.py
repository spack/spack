# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyBintrees(PythonPackage):
    """Package provides Binary-, RedBlack- and AVL-Trees in Python and Cython.
    """

    homepage = "https://github.com/mozman/bintrees"
    pypi = "bintrees/bintrees-2.0.7.zip"

    version('2.2.0', sha256='e180658d90789855dcb0e7d1eb2bfebc452d60c5b48e74de16b502d61a8352d1')
    version('2.1.0', sha256='eae2732fae01b24eb17b3943721945c1ec88b2126e081c5c785ce448924d3f96')
    version('2.0.7', sha256='60675e6602cef094abcd38bf4aecc067d78ae2d5e1645615c789724542d11270')

    depends_on('py-setuptools', type='build')

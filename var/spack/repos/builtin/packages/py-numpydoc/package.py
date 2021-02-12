# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyNumpydoc(PythonPackage):
    """numpydoc - Numpy's Sphinx extensions"""

    homepage = "https://github.com/numpy/numpydoc"
    pypi = "numpydoc/numpydoc-0.6.0.tar.gz"

    version('1.1.0', sha256='c36fd6cb7ffdc9b4e165a43f67bf6271a7b024d0bb6b00ac468c9e2bfc76448e')
    version('1.0.0', sha256='e481c0799dfda208b6a2c2cb28757fa6b6cbc4d6e43722173697996cf556df7f')
    version('0.9.2', sha256='9140669e6b915f42c6ce7fef704483ba9b0aaa9ac8e425ea89c76fe40478f642')
    version('0.9.1', sha256='e08f8ee92933e324ff347771da15e498dbf0bc6295ed15003872b34654a0a627')
    version('0.9.0', sha256='45e897ffc7f3e6962f6a02ea996d1661d99011f3d68fee450dc33056b60da84e')
    version('0.8.0', sha256='61f4bf030937b60daa3262e421775838c945dcdd671f37b69e8e4854c7eb5ffd')
    version('0.7.0', sha256='2dc7b2c4e3914745e38e370946fa4c109817331e6d450806285c08bce5cd575a')
    version('0.6.0', sha256='1ec573e91f6d868a9940d90a6599f3e834a2d6c064030fbe078d922ee21dcfa1')

    depends_on('python@2.6:2.8,3.3:')
    depends_on('py-setuptools',    type='build')
    depends_on('py-sphinx@1.0.1:', type='build')

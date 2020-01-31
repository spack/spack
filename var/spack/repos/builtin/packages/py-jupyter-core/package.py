# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyJupyterCore(PythonPackage):
    """Core Jupyter functionality"""

    homepage = "http://jupyter-core.readthedocs.io/"
    url      = "https://github.com/jupyter/jupyter_core/archive/4.2.0.tar.gz"

    version('4.4.0', sha256='a3c693cb4cd1251f887f034eba4b74e5ad1beab5baef43cc3ae9387450e72367')
    version('4.2.0', sha256='ca2db4bc44b870ad9039bfdcad81bb0466e6bf0e6e2e03626815977ee73dc7a7')
    version('4.1.1', sha256='1908dd9eceb8994c1f0b1bb81c20a52dbb01692e4f1fdf5d12e04846b94eb05c')
    version('4.1.0', sha256='80b78d215399760f4678cc1512118257543e17b48316254d1e1dbddfafa2dffc')
    version('4.0.6', sha256='76d9f95eec679d1ce8a07fba4e373bda3b17ca89e3b03ee6186a7dbdc117d7e8')
    version('4.0.5', sha256='783c2be522010db9dd0ff54c28fcdf31afe73a5f7d956eb89ddce2c48f381548')
    version('4.0.4', sha256='ee81c1e2c67afe0b9c1097043f76063b452670fc63377ab4656ce1b2826cd166')
    version('4.0.3', sha256='5ecc177e8c711a410f857adc65f8413b06ea1f2fa2330559a723d6c1981852f8')
    version('4.0.2', sha256='ad2f537aacaa9978b37ac5d39d9bd582d2a9dfc104b3d289b88687c1c5a0ece0')
    version('4.0.1', sha256='faa3878b286f63d1853aec3e4b80e2a7299f580a9acebd4a1cafa36b264ec0a3')
    version('4.0',   sha256='2b491a5da687ffab4e5702e37d3cb8b6b184cd46520cae9c459bdb1fd144f026')

    depends_on('python@2.7:2.8,3.3:')
    depends_on('py-traitlets', type=('build', 'run'))

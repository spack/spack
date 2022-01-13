# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyTmd(PythonPackage):
    """Python library for the topological analysis of neurons"""

    homepage = "https://github.com/BlueBrain/TMD"
    url = "https://pypi.io/packages/source/t/tmd/tmd-2.0.9.tar.gz"

    version('2.0.11', sha256='ba19167d19eb2132af766b760a6f09f423abbdcf871c23c2bfdf8c9064ba888e')
    version('2.0.9', sha256='9bfb4b014e2c735c9db5f3ee61e4ccdbac29248f608ba49a43d862e4835b88a5')
    version('2.0.8', sha256='56373aa32f2cc201b083760cf5110749f7d6fd488603a5809e6af8c312c1a77e')
    version('2.0.4', sha256='b1709f36964d11dd555a35f99dfa26187ce2ef98a56f07eaa4805da944e86652')
    version('2.0.3', sha256='ffde39a2fa6221a093ff66390a205149348e97a459aba1ab8f04998070e00dc1')

    depends_on('py-setuptools', type='build')

    depends_on('py-cached-property', type=('build', 'run'))
    depends_on('py-enum34@1.0:', type=('build', 'run'), when='^python@:3.3.99')
    depends_on('py-h5py@2.8:', type=('build', 'run'))
    depends_on('py-morphio@2.7.1:', type=('build', 'run'))
    depends_on('py-munkres@1.0.12:', type=('build', 'run'))
    depends_on('py-numpy@1.8:', type=('build', 'run'))
    depends_on('py-scikit-learn@0.19:', type=('build', 'run'))
    depends_on('py-scipy@0.13:', type=('build', 'run'))

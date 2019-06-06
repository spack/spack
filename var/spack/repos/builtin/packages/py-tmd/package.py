# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyTmd(PythonPackage):
    """Python library for the topological analysis of neurons"""

    homepage = "https://github.com/BlueBrain/TMD"
    url = "https://pypi.io/packages/source/t/tmd/tmd-2.0.3.tar.gz"

    version('2.0.4', sha256='b1709f36964d11dd555a35f99dfa26187ce2ef98a56f07eaa4805da944e86652', preferred=True)
    version('2.0.3', sha256='ffde39a2fa6221a093ff66390a205149348e97a459aba1ab8f04998070e00dc1')

    depends_on('py-setuptools', type='build')

    depends_on('py-enum34@1.0:', type='run', when='^python@:3.3.99')
    depends_on('py-h5py@2.8:', type='run')
    depends_on('py-munkres@1.0.12:', type='run')
    depends_on('py-numpy@1.8:', type='run')
    depends_on('py-scikit-learn@0.19:', type='run')
    depends_on('py-scipy@0.13:', type='run')

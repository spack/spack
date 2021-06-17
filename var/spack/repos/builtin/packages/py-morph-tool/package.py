# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyMorphTool(PythonPackage):
    """Python morphology manipulation toolkit"""

    homepage = "https://github.com/BlueBrain/morph-tool"
    git      = "https://github.com/BlueBrain/morph-tool.git"
    url      = "https://pypi.io/packages/source/m/morph-tool/morph-tool-2.4.1.tar.gz"

    version('develop', branch='master')
    version('2.6.0', sha256='5f3c0e6f2402631d499629ffd95ce9ddc09745f0f1892901d67d338a016b7ea1')
    version('2.5.1', sha256='bffe0d4ec4cd0e98bce5efc8af01a7ccb06b5787f379d420bc154c58067134d0')
    version('2.4.7', sha256='d95ce62309e9594d9241852e3c9e39462b05bd71fb781090da6235cb471459d9')
    version('2.4.1', sha256='b1db7837c73ca27c7e596e3461104b0ae0d9036a48d41cae2d79a7e7d7a4f451')

    depends_on('py-setuptools', type=('build', 'run'))

    depends_on('py-click@6.7:', type='run')
    depends_on('py-deprecation@2.1.0:', type='run')
    depends_on('py-more-itertools@8.6.0:', type='run')
    depends_on('py-numpy@1.14:', type='run')
    depends_on('py-pandas@1.0.3:', type='run')
    depends_on('py-xmltodict@0.12:', type='run')

    depends_on('py-plotly@4.1:', type='run')
    depends_on('py-dask+bag@2.19:', type='run')
    depends_on('neuron+python@7.8:', type='run')
    depends_on('py-bluepyopt@1.9.37:', type='run')

    depends_on('py-neurom@2.0:2.999', type='run', when='@2.5.1:')
    depends_on('py-neurom@1.8:1.999', type='run', when='@:2.4.99')
    depends_on('py-morphio@3.0:3.999', type='run', when='@2.5.1:')
    depends_on('py-morphio@2.7.0:2.999', type='run', when='@:2.4.99')

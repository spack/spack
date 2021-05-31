# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyMorphTool(PythonPackage):
    """Python morphology manipulation toolkit"""

    homepage = "https://github.com/BlueBrain/morph-tool"
    git      = "https://github.com/BlueBrain/morph-tool.git"
    url      = "https://pypi.io/packages/source/m/morph-tool/morph-tool-2.4.4.tar.gz"

    version('develop', branch='master')
    version('2.5.0', sha256='279123b59797132a2e4f8fd9df391279fce85891dec046bd1206de4c7d4f8e11')
    version('2.4.4', sha256='15feab33270e20f423136c36be2cf0ae217591519ae72244b25ad8e0a163af9c')
    version('2.4.1', sha256='b1db7837c73ca27c7e596e3461104b0ae0d9036a48d41cae2d79a7e7d7a4f451')

    depends_on('py-setuptools', type=('build', 'run'))

    depends_on('py-click@6.7:', type='run')
    depends_on('py-deprecation@2.1.0:', type='run')
    depends_on('py-more-itertools@8.6.0:', type='run')
    depends_on('py-morphio@2.7.0:', type='run')
    depends_on('py-numpy@1.14:', type='run')
    depends_on('py-pandas@1.0.3:', type='run')
    depends_on('py-xmltodict@0.12:', type='run')

    depends_on('py-plotly@4.1:', type='run')
    depends_on('py-dask+bag@2.19:', type='run')
    depends_on('neuron+python@7.8:', type='run')
    depends_on('py-bluepyopt@1.9.37:', type='run')

    depends_on('py-neurom@2.0:2.999', type='run', when='@2.4.4:')
    depends_on('py-neurom@1.8:1.999', type='run', when='@:2.4.1')

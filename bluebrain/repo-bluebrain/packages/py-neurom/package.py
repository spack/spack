# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyNeurom(PythonPackage):
    """Python library neuron morphology analysis"""

    homepage = "https://github.com/BlueBrain/NeuroM"
    git = "https://github.com/BlueBrain/NeuroM.git"
    url = "https://pypi.io/packages/source/n/neurom/neurom-2.2.1.tar.gz"

    version('develop', branch='master')
    version('3.0.0',  sha256='05f5f5c4292dfa23f3319347cf2a7c147732ba0140b9db0bc94e535ac74be8da')

    variant('plotly', default=False, description="Enable plotly support")

    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('py-click@7.0:', type=('build', 'run'))
    depends_on('py-numpy@1.8.0:', type=('build', 'run'))
    depends_on('py-pyyaml@3.10:', type=('build', 'run'))
    depends_on('py-tqdm@4.8.4:', type=('build', 'run'))
    depends_on('py-matplotlib@3.2.1:', type=('build', 'run'))
    depends_on('py-scipy@1.2.0:', type=('build', 'run'))
    depends_on('py-plotly@3.6.0:', type='run', when='+plotly')

    depends_on('py-morphio@3.1.1:', type=('build', 'run'))
    depends_on('py-pandas@1.0.5:', type=('build', 'run'))

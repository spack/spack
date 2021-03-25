# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyNeurom(PythonPackage):
    """Python library neuron morphology analysis"""

    homepage = "https://github.com/BlueBrain/NeuroM"
    git = "https://github.com/BlueBrain/NeuroM.git"
    url = "https://pypi.io/packages/source/n/neurom/neurom-1.8.0.tar.gz"

    version('develop', branch='master')
    version('1.8.0',  sha256='d364d3b184bd96cbe5fa601ae24f6b7d431fa42de646e3011a33d56f3cfc247c')
    version('1.7.0',  sha256='713d874538f1c566b57ab81e0558726fc6d4b7de91301a6be495776c55ac47f8')
    version('1.6.0',  sha256='74759199c5392ae8e209f037a5046646d06ec1f77b1cd826afac71eeeca0f7ab')
    version('1.5.0',  sha256='40a4362b58cbbbac769a1cef5b6e5e6ececbf4b538d81c0ed23fe421645aa3c4')

    variant('plotly', default=False, description="Enable plotly support")

    depends_on('py-setuptools', type=('build', 'run'))

    # common
    depends_on('py-click@7.0:', type='run')
    depends_on('py-numpy@1.8.0:', type='run')
    depends_on('py-pyyaml@3.10:', type='run')
    depends_on('py-tqdm@4.8.4:', type='run')
    depends_on('py-matplotlib@3.2.1:', type='run')
    depends_on('py-scipy@1.2.0:', type='run')
    depends_on('py-plotly@3.6.0:', type='run', when='+plotly')

    # >= 1.6.0, < 2.0
    depends_on('py-h5py@3.1.0:', type='run', when='@1.6:1.999')
    depends_on('py-pandas@1.0.5:', type='run', when='@1.6:1.999')

    # < 1.6.0
    depends_on('py-h5py@2.7.1:2.999', type='run', when='@:1.5.999')

# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyNeurom(PythonPackage):
    """Python library neuron morphology analysis"""

    homepage = "https://github.com/BlueBrain/NeuroM"
    git = "https://github.com/BlueBrain/NeuroM.git"
    url = "https://pypi.io/packages/source/n/neurom/neurom-1.4.10.tar.gz"

    version('develop', branch='master')
    version('mut_morphio', branch='mut_morphio')
    version('1.7.0',  sha256='713d874538f1c566b57ab81e0558726fc6d4b7de91301a6be495776c55ac47f8')
    version('1.6.0',  sha256='74759199c5392ae8e209f037a5046646d06ec1f77b1cd826afac71eeeca0f7ab')
    version('1.5.0',  sha256='40a4362b58cbbbac769a1cef5b6e5e6ececbf4b538d81c0ed23fe421645aa3c4')
    version('1.4.20', sha256='c867764511dbb6d2e276a6ac517322ac56bf0a2f85047a96afd60b0f7f54153d')
    version('1.4.15', sha256='d84f04c292ed9b2fe1d34d6e754a133f69ef81a038947d836dd4f34ccd7b4607')
    version('1.4.14', sha256='e541f6c8a11826caa2b2d1cf18015a10ec7009f12813edfc2655084c7cf5021b')
    version('1.4.10', sha256='c94823133bb15b5756c22391e05948871ff77c0212e91ad375903ca437e18aeb')

    variant('plotly', default=False, description="Enable plotly support")

    depends_on('py-click@7.0:', type='run')
    depends_on('py-enum34@1.0.4:', type='run', when='@:1.4.999 ^python@:3.3.99')
    depends_on('py-future@0.16.0:', type='run', when='@:1.4.999')
    depends_on('py-h5py~mpi@2.7.1:', type='run')
    depends_on('py-matplotlib@1.3.1:', type='run')
    depends_on('py-morphio@2.3.10:', type='run', when='@mut_morphio')
    depends_on('py-numpy@1.8.0:', type='run')
    depends_on('py-plotly@3.0.0:', type='run', when='+plotly')
    depends_on('py-pylru@1.0:', type='run', when='@:1.4.999')
    depends_on('py-pyyaml@3.10:', type='run')
    depends_on('py-scipy@0.17.0:', type='run')
    depends_on('py-tqdm@4.8.4:', type='run')
    depends_on('py-setuptools', type=('build', 'run'))

    conflicts('^python@:3.3.99', when='@1.5:')

    def patch(self):
        if self.spec.satisfies('^python@:3.0'):
            filter_file(r'matplotlib>=1.3.1', r'matplotlib<3.0', "setup.py")
            filter_file(r"'scipy>=.*'", r"'scipy<1.3'", "setup.py")

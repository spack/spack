# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyNeurom(PythonPackage):
    """Python library neuron morphology analysis"""

    homepage = "https://github.com/BlueBrain/NeuroM"
    url = "https://pypi.io/packages/source/n/neurom/neurom-1.4.10.tar.gz"

    version('1.4.10', sha256='c94823133bb15b5756c22391e05948871ff77c0212e91ad375903ca437e18aeb', preferred=True)

    variant('plotly', default=False, description="Enable plotly support")

    depends_on('py-click@7.0:', type='run')
    depends_on('py-enum34@1.0.4:', type='run', when='^python@:3.3.99')
    depends_on('py-future@0.16.0:', type='run')
    depends_on('py-h5py~mpi@2.7.1:', type='run')
    depends_on('py-matplotlib@1.3.1:', type='run')
    depends_on('py-numpy@1.8.0:', type='run')
    depends_on('py-plotly@3.0.0', type='run', when='+plotly')
    depends_on('py-pylru@1.0:', type='run')
    depends_on('py-pyyaml@3.10:', type='run')
    depends_on('py-scipy@0.17.0:', type='run')
    depends_on('py-tqdm@4.8.4:', type='run')

    def patch(self):
        if self.spec.satisfies('^python@:3.0'):
            filter_file(r'matplotlib>=1.3.1', r'matplotlib<3.0', "setup.py")
            filter_file(r'scipy>=0.17.0', r'scipy<1.3', "setup.py")

# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyAibsCircuitConverter(PythonPackage):
    """Pythonic API for conversion between Allen Institute and BBP"""

    homepage = "https://bbpgitlab.epfl.ch/nse/aibs-circuit-converter"
    git      = "git@bbpgitlab.epfl.ch:nse/aibs-circuit-converter.git"

    version('develop', branch='master')
    version('0.0.3', tag='aibs-circuit-converter-v0.0.3')
    version('0.0.1', tag='aibs-circuit-converter-v0.0.1')

    depends_on('py-setuptools', type=('build', 'run'))

    depends_on('py-numpy@1.14:', type='run')
    depends_on('py-h5py@2.8:', type='run')
    depends_on('py-pandas@0.25:', type='run')
    depends_on('py-lxml@4.3.4:', type='run')
    depends_on('py-tqdm@4.34:', type='run')
    depends_on('py-transforms3d@0.3:', type='run')
    depends_on('py-six@1.0:', type='run')
    depends_on('py-bluepyopt@1.8.68:', type='run')

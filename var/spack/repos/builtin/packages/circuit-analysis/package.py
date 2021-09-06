# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class CircuitAnalysis(PythonPackage):
    """Pythonic Sonata circuit reduction API"""

    homepage = "https://bbpgitlab.epfl.ch/nse/circuit-analysis"
    git      = "git@bbpgitlab.epfl.ch:nse/circuit-analysis.git"

    version('develop', branch='master')
    version('0.0.5', tag='circuit-analysis-v0.0.5')

    depends_on('py-setuptools', type=('build', 'run'))

    depends_on('py-click@7.0:', type='run')
    depends_on('py-numpy@1.9:', type='run')
    depends_on('py-pandas@0.17:', type='run')
    depends_on('py-matplotlib@2.0:', type='run')
    depends_on('py-seaborn@0.8:', type='run')
    depends_on('py-bluepy@2:', type='run')
    depends_on('py-neurom@1.6:', type='run')
    depends_on('py-joblib@0.14:', type='run')
    depends_on('py-libsonata@0.1.4:', type='run')
    depends_on('py-tqdm@4.3:', type='run')
    depends_on('py-lxml@3.3.2:', type='run')

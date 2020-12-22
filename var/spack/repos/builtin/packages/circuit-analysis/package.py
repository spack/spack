# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class CircuitAnalysis(PythonPackage):
    """Pythonic Sonata circuit reduction API"""

    homepage = "https://bbpcode.epfl.ch/code/#/admin/projects/nse/circuit-analysis"
    git      = "ssh://bbpcode.epfl.ch/nse/circuit-analysis"

    version('develop', branch='master')
    version('0.0.4', tag='circuit-analysis-v0.0.4')

    depends_on('py-setuptools', type=('build', 'run'))

    depends_on('py-click@7.0:', type='run')
    depends_on('py-numpy@1.9:', type='run')
    depends_on('py-pandas@0.17:', type='run')
    depends_on('py-matplotlib@2.0:', type='run')
    depends_on('py-seaborn@0.8:', type='run')
    depends_on('py-bluepy@0.14:0.99', type='run')
    depends_on('py-neurom@1.0:1.5.99', type='run')
    depends_on('py-joblib@0.14:', type='run')
    depends_on('py-libsonata@0.1.4:', type='run')
    depends_on('py-tqdm@4.3:', type='run')

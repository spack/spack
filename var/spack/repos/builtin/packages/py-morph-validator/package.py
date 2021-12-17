# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class PyMorphValidator(PythonPackage):
    """Python library neuron morphology analysis"""

    homepage = "https://bbpgitlab.epfl.ch/nse/morph-validator"
    git      = "git@bbpgitlab.epfl.ch:nse/morph-validator.git"
    version('develop')
    version('0.3.0', tag='morph-validator-v0.3.0')

    depends_on('py-setuptools', type=('build', 'run'))

    depends_on('py-pandas@0.25:1.2.99', type=('build', 'run'))
    depends_on('py-joblib@0.14:', type=('build', 'run'))
    depends_on('py-numpy@1.14:', type=('build', 'run'))
    depends_on('py-scipy@1.3:', type=('build', 'run'))
    depends_on('py-lxml@4.3.4:', type=('build', 'run'))
    depends_on('py-morph-tool@2.9.0:2.999', type=('build', 'run'))
    depends_on('py-neurom@3.0:3.999', type=('build', 'run'))
    depends_on('py-bluepy@2.3.0:2.99', type=('build', 'run'))
    depends_on('py-seaborn@0.10.1:', type=('build', 'run'))
    depends_on('py-tqdm@4.46.0:', type=('build', 'run'))
    depends_on('py-matplotlib@2.2.0:', type=('build', 'run'))

# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyDhScikitOptimize(PythonPackage):
    """A Modified version of scikit-optimize a Sequential model-based
       optimization toolbox for DeepHyper.
       Scikit-Optimize, or skopt, is a simple and efficient library to
       minimize (very) expensive and noisy black-box functions. It implements
       several methods for sequential model-based optimization. skopt aims to
       be accessible and easy to use in many contexts.

       The library is built on top of NumPy, SciPy and Scikit-Learn."""

    maintainers = ['Kerilk']

    homepage = "https://github.com/deephyper/scikit-optimize"
    pypi     = "dh-scikit-optimize/dh-scikit-optimize-0.9.0.tar.gz"

    version('0.9.0', sha256='fe70aa57ec5150a3d356b2184f0dda1ecc4ecb7e82d35edac3980094d409d676')

    variant('plots', default=False,
            description='Build with plot support from py-matplotlib')

    depends_on('python@3.6:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-joblib@0.11:', type=('build', 'run'))
    depends_on('py-pyaml@16.9:', type=('build', 'run'))
    depends_on('py-numpy@1.13.3:', type=('build', 'run'))
    depends_on('py-scipy@0.19.1:', type=('build', 'run'))
    depends_on('py-scikit-learn@0.20.0:', type=('build', 'run'))
    depends_on('py-configspace@0.4.20:', type=('build', 'run'))

    depends_on('py-matplotlib@2.0.0:',   when='+plots', type='run')

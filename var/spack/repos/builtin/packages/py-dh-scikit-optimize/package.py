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

    version('0.9.4', sha256='9acfba4077fe45f3854a4af255763a3e8a396c05bd2a7c761a969171366b3840')
    version('0.9.0', sha256='fe70aa57ec5150a3d356b2184f0dda1ecc4ecb7e82d35edac3980094d409d676')

    variant('plots', default=True,
            description='Build with plot support from py-matplotlib')

    depends_on('python@3.6:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-scipy', type=('build', 'run'))
    depends_on('py-scikit-learn', type=('build', 'run'))
    depends_on('py-pyaml', type=('build', 'run'))
    depends_on('py-config-space', type=('build', 'run'))

    depends_on('py-matplotlib',   when='+plots')

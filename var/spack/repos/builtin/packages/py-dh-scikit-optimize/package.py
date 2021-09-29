# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyDhScikitOptimize(PythonPackage):
    """Scikit-Optimize, or skopt, is a simple and efficient library to
       minimize (very) expensive and noisy black-box functions. It implements
       several methods for sequential model-based optimization. skopt aims to
       be accessible and easy to use in many contexts.

       The library is built on top of NumPy, SciPy and Scikit-Learn."""

    homepage = "https://github.com/deephyper/scikit-optimize"
    url      = "https://github.com/deephyper/scikit-optimize/archive/refs/tags/0.9.0.tar.gz"

    version('0.9.0', sha256='d592db43bdaba300cd2433c08536119fa56d09b8be81922b0347d95dbd3f6250')

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

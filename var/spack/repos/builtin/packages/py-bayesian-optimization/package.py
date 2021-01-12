# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyBayesianOptimization(PythonPackage):
    """Pure Python implementation of bayesian global
    optimization with gaussian processes."""

    homepage = "https://github.com/fmfn/BayesianOptimization"
    url      = "https://github.com/fmfn/BayesianOptimization/archive/1.2.0.tar.gz"

    version('1.2.0', sha256='34e2444ec0649fd3391738fd388a6bed82a8c0a3702d53d18e8eb3a57b415b38')

    depends_on('py-setuptools', type='build')
    depends_on("py-numpy@1.9.0:", type=('build', 'run'))
    depends_on("py-scipy@0.14.0:", type=('build', 'run'))
    depends_on("py-scikit-learn@0.18.0:", type=('build', 'run'))

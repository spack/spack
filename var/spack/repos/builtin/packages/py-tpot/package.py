# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyTpot(PythonPackage):
    """
    A Python Automated Machine Learning tool that optimizes machine learning
    pipelines using genetic programming.
    """

    homepage = "http://epistasislab.github.io/tpot/"
    url      = "https://pypi.io/packages/source/t/tpot/TPOT-0.11.5.tar.gz"

    version('0.11.5', sha256='909be08b29165ce48de5e5d2e3fd73fee9aeeaf1030f2e0912ce0f0bd9c3d2f3')

    depends_on('py-setuptools',     type='build')
    depends_on('python@3.5:',       type=('build', 'run'))
    depends_on('py-deap',           type=('build', 'run'))
    depends_on('py-nose',           type='test')
    depends_on('py-numpy',          type=('build', 'run'))
    depends_on('py-scikit-learn',   type=('build', 'run'))
    depends_on('py-scipy',          type=('build', 'run'))
    depends_on('py-tqdm',           type=('build', 'run'))
    depends_on('py-stopit',         type=('build', 'run'))
    depends_on('py-pandas',         type=('build', 'run'))
    depends_on('py-joblib',         type=('build', 'run'))

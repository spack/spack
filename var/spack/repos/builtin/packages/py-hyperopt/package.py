# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyHyperopt(PythonPackage):
    """Hyperopt is a Python library for serial and parallel optimization over
    awkward search spaces, which may include real-valued, discrete, and
    conditional dimensions."""

    homepage = "http://hyperopt.github.io/hyperopt/"
    pypi     = "hyperopt/hyperopt-0.2.5.tar.gz"

    version('0.2.5', sha256='bc6047d50f956ae64eebcb34b1fd40f186a93e214957f20e87af2f10195295cc')
    version('0.2.4', sha256='6e72089a42eb70cf84b0567d4552a908adff7cfc5cf6b1c38add41adc775d9c6')

    depends_on('python@2.7:',       type=('build', 'run'))
    depends_on('py-setuptools',     type='build')
    depends_on('py-numpy',          type=('build', 'run'))
    depends_on('py-scipy',          type=('build', 'run'))
    depends_on('py-six',            type=('build', 'run'))
    depends_on('py-networkx@2.2:',  type=('build', 'run'))
    depends_on('py-future',         type=('build', 'run'))
    depends_on('py-tqdm',           type=('build', 'run'))
    depends_on('py-cloudpickle',    type=('build', 'run'))
    depends_on('py-pyspark',        type=('build', 'run'))
    depends_on('py-pymongo',        type=('build', 'run'))
    depends_on('py-scikit-learn',   type=('build', 'run'))

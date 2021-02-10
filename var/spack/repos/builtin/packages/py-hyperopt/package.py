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
    version('0.2.3', sha256='df450eadfc9541086921bf863a5842e7009faef472b08630fd2cab13cdcfe0e6')
    version('0.2.2', sha256='cb79b9877723be7b4cf0cb6911525ebaf36edbce5e09d09d672a43ff22fdc455')
    version('0.2.1', sha256='ae8e56011642ebdaf329fd46dc0f565f6afd7db75d509120b4e0c186c8394bed')
    version('0.2',   sha256='011c8e811c8353ddf3dfff1ddf53712d54a9f182f12f66166b3a0cc15504091f')
    version('0.1.2', sha256='df8c48a62bc1614bdc37f5cc570064a93a4b81a16559621db9acee3f6536b658')
    version('0.1',   sha256='4f6e903f7640165ea3e4c622050b41ffab0bee7811ede23c7825a5884976d72f')
    version('0.0.2', sha256='35b1ddfb9c2b16884f513c9ed342cf2be04af85ea8c231b5230d406320f20bd5')
    version('0.0.1', sha256='0e224af6710855ddfa34df5e44a1251387fa24e49e090c97d9f1b0bb16cda05d')

    depends_on('python@2.7:',       type=('build', 'run'))
    depends_on('py-setuptools',     type='build')
    depends_on('py-numpy',          type=('build', 'run'))
    depends_on('py-scipy',          type=('build', 'run'))
    depends_on('py-six',            type=('build', 'run'))
    depends_on('py-networkx@2.2:',  type=('build', 'run'))
    depends_on('py-future',         type=('build', 'run'))
    depends_on('py-tqdm',           type=('build', 'run'))
    depends_on('py-cloudpickle',    type=('build', 'run'))
    depends_on('py-pyspark@3.0.1',        type=('build', 'run'))
    depends_on('py-pymongo',        type=('build', 'run'))
    depends_on('py-scikit-learn',   type=('build', 'run'))

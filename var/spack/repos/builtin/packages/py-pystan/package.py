# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPystan(PythonPackage):
    """PyStan is a Python interface to Stan, a package for Bayesian inference."""

    homepage = "https://mc-stan.org/"
    pypi     = "pystan/pystan-3.4.0.tar.gz"

    maintainers = ['haralmha']

    version('3.4.0', sha256='325e2fb0ab804555c05a603e0c9152ab11fcc3af01f3e9a9ff9fe9954b93184f')

    depends_on('python@3.8:3', type=('build', 'run'))
    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('py-poetry-core@1.0.0:', type='build')
    depends_on('py-aiohttp@3.6:3', type=('build', 'run'))
    depends_on('py-httpstan@4.7', type=('build', 'run'))
    depends_on('py-pysimdjson@3.2:3', type=('build', 'run'))
    depends_on('py-numpy@1.19:1', type=('build', 'run'))
    depends_on('py-clikit@0.6:0', type=('build', 'run'))

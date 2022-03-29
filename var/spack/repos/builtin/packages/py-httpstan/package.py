# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyHttpstan(PythonPackage):
    """HTTP-based REST interface to Stan, a package for Bayesian inference."""

    homepage = "https://mc-stan.org/"
    url      = "https://github.com/stan-dev/httpstan/archive/refs/tags/4.6.1.tar.gz"

    maintainers = ['haralmha']

    version('4.6.1', sha256='703e5e04e60651e0004574bb9695827d759fd13eb0d6bd67f827c1bfa0a1fd31')

    depends_on('python@3.7:', type=('build', 'run'))
    depends_on('py-setuptools@41.0:', type='build')
    depends_on('py-poetry-core@1.0.0:', type='build')
    depends_on('py-aiohttp@3.7:', type=('build', 'run'))
    depends_on('py-appdirs@1.4:', type=('build', 'run'))
    depends_on('py-webargs@8.0:', type=('build', 'run'))
    depends_on('py-marshmallow@3.10:', type=('build', 'run'))
    depends_on('py-numpy@1.16:', type=('build', 'run'))
    depends_on('py-pybind11')

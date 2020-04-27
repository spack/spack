# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyWheel(PythonPackage):
    """A built-package format for Python."""

    homepage = "https://pypi.python.org/pypi/wheel"
    url      = "https://pypi.io/packages/source/w/wheel/wheel-0.29.0.tar.gz"

    version('0.33.4', sha256='62fcfa03d45b5b722539ccbc07b190e4bfff4bb9e3a4d470dd9f6a0981002565')
    version('0.33.1', sha256='66a8fd76f28977bb664b098372daef2b27f60dc4d1688cfab7b37a09448f0e9d')
    version('0.32.3', sha256='029703bf514e16c8271c3821806a1c171220cc5bdd325cbf4e7da1e056a01db6')
    version('0.29.0', sha256='1ebb8ad7e26b448e9caa4773d2357849bf80ff9e313964bcaf79cbf0201a1648')
    version('0.26.0', sha256='eaad353805c180a47545a256e6508835b65a8e830ba1093ed8162f19a50a530c')

    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('python@2.7:2.8,3.4:', type=('build', 'run'))
    depends_on('py-pytest@3.0.0:', type='test')
    depends_on('py-pytest-cov', type='test')

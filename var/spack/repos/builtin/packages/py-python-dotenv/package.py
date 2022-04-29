# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.pkgkit import *


class PyPythonDotenv(PythonPackage):
    """Read key-value pairs from a .env file and set them as environment variables"""

    homepage = "https://github.com/theskumar/python-dotenv"
    pypi = "python-dotenv/python-dotenv-0.19.2.tar.gz"

    maintainers = ['jcpunk']

    version('0.19.2', sha256='a5de49a31e953b45ff2d2fd434bbc2670e8db5273606c1e737cc6b93eff3655f')

    variant('cli', default=False, description="Add commandline tools")

    depends_on('python@3.5:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')

    depends_on('py-click@5:', when="+cli", type=('build', 'run'))

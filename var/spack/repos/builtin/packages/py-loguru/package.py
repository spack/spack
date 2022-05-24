# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyLoguru(PythonPackage):
    """Loguru is a library which aims to bring enjoyable logging in Python."""

    homepage = "https://github.com/Delgan/loguru"
    pypi     = "loguru/loguru-0.6.0.tar.gz"

    version('0.6.0', sha256='066bd06758d0a513e9836fd9c6b5a75bfb3fd36841f4b996bc60b547a309d41c')

    depends_on('python@3.5:', type='build')
    depends_on('py-aiocontextvars@0.2.0:', when='^python@3.6:')
    depends_on('py-win32-setctime@1.0.0:', when='platform=win32')
    depends_on('py-colorama@0.3.4:')
    depends_on('py-black@19.10b0:', when='^python@3.6:')
    depends_on('py-docutils@0.16')
    depends_on('py-flake8@3.7.7:')
    depends_on('py-isort@5.1.1:', when='^python@3.6:')
    depends_on('py-tox@3.9.0:')
    depends_on('py-pytest@4.6.2:')
    depends_on('py-pytest-cov@2.7.1:')
    depends_on('py-sphinx@4.1.1:', when='^python@3.6:')
    depends_on('py-sphinx-autobuild@0.7.1:', when ='^python@3.6:')
    depends_on('py-sphinx-rtd-theme@0.4.3:', when='^python@3.6:')

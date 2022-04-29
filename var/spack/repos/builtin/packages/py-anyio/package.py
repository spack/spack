# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.pkgkit import *


class PyAnyio(PythonPackage):
    """High level compatibility layer for multiple asynchronous event loop
       implementations."""

    homepage = "https://github.com/agronholm/anyio"
    pypi     = "anyio/anyio-3.2.1.tar.gz"

    version('3.5.0', sha256='a0aeffe2fb1fdf374a8e4b471444f0f3ac4fb9f5a5b542b48824475e0042a5a6')
    version('3.3.4', sha256='67da67b5b21f96b9d3d65daa6ea99f5d5282cb09f50eb4456f8fb51dffefc3ff')
    version('3.2.1', sha256='07968db9fa7c1ca5435a133dc62f988d84ef78e1d9b22814a59d1c62618afbc5')

    depends_on('python@3.6.2:', type=('build', 'run'))
    depends_on('py-setuptools@42:', type='build')
    depends_on('py-setuptools-scm+toml@3.4:', type='build')
    depends_on('py-wheel@0.29:', type='build')
    depends_on('py-contextvars', when='@3.4: ^python@:3.6', type=('build', 'run'))
    depends_on('py-dataclasses', when='^python@:3.6', type=('build', 'run'))
    depends_on('py-idna@2.8:', type=('build', 'run'))
    depends_on('py-sniffio@1.1:', type=('build', 'run'))
    depends_on('py-typing-extensions', when='^python@:3.7', type=('build', 'run'))

    depends_on('py-async-generator', when='@:3.2 ^python@:3.6', type=('build', 'run'))

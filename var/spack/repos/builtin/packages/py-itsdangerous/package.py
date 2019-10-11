# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyItsdangerous(PythonPackage):
    """Various helpers to pass trusted data to untrusted environments."""

    homepage = "http://github.com/mitsuhiko/itsdangerous"
    url = "https://pypi.io/packages/source/i/itsdangerous/itsdangerous-0.24.tar.gz"

    version('0.24', sha256='cbb3fcf8d3e33df861709ecaf89d9e6629cff0a217bc2848f1b41cd30d360519')

    depends_on('py-setuptools', type='build')

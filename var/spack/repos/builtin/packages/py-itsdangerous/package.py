# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyItsdangerous(PythonPackage):
    """Various helpers to pass trusted data to untrusted environments."""

    homepage = "http://github.com/mitsuhiko/itsdangerous"
    url = "https://pypi.io/packages/source/i/itsdangerous/itsdangerous-0.24.tar.gz"

    version('0.24', 'a3d55aa79369aef5345c036a8a26307f')

    depends_on('py-setuptools', type='build')

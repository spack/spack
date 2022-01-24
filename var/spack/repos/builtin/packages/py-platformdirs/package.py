# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPlatformdirs(PythonPackage):
    """A small Python module for determining appropriate
       platform-specific dirs, e.g. a "user data dir" """

    homepage = "https://github.com/platformdirs/platformdirs"
    pypi     = "platformdirs/platformdirs-2.4.0.tar.gz"

    version('2.4.0', sha256='367a5e80b3d04d2428ffa76d33f124cf11e8fff2acdaa9b43d545f5c7d661ef2')

    depends_on('python@3.6:', type=('build', 'run'))
    depends_on('py-setuptools@44:', type='build')
    depends_on('py-setuptools-scm@5:+toml', type='build')

# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package_defs import *


class PyTomlkit(PythonPackage):
    """Style preserving TOML library"""

    homepage = "https://github.com/sdispater/tomlkit"
    pypi = "tomlkit/tomlkit-0.7.0.tar.gz"

    version('0.7.2', sha256='d7a454f319a7e9bd2e249f239168729327e4dd2d27b17dc68be264ad1ce36754')
    version('0.7.0', sha256='ac57f29693fab3e309ea789252fcce3061e19110085aa31af5446ca749325618')

    depends_on('python@2.7,3.5:', type=('build', 'run'))
    depends_on('py-poetry-core@1:', type='build')
    depends_on('py-enum34@1.1:1', when='^python@2.7', type=('build', 'run'))
    depends_on('py-functools32@3.2.3:3', when='^python@2.7', type=('build', 'run'))
    depends_on('py-typing@3.6:3', when='^python@2.7,3.4', type=('build', 'run'))

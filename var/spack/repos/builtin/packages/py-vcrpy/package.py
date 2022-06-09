# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyVcrpy(PythonPackage):
    """Automatically mock your HTTP interactions to simplify and speed up testing."""

    homepage = "https://github.com/kevin1024/vcrpy"
    pypi     = "vcrpy/vcrpy-4.1.1.tar.gz"

    version('4.1.1', sha256='57095bf22fc0a2d99ee9674cdafebed0f3ba763018582450706f7d3a74fff599')

    depends_on('python@3.5:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-pyyaml', type=('build', 'run'))
    depends_on('py-wrapt', type=('build', 'run'))
    depends_on('py-six@1.5:', type=('build', 'run'))
    depends_on('py-yarl', when='^python@3.6:', type=('build', 'run'))
    depends_on('py-yarl@:1.3', when='^python@3.5', type=('build', 'run'))

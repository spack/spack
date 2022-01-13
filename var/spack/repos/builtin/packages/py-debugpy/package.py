# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyDebugpy(PythonPackage):
    """An implementation of the Debug Adapter Protocol for Python."""

    homepage = "https://github.com/microsoft/debugpy/"
    pypi     = "debugpy/debugpy-1.4.1.zip"

    # 'debugpy._vendored' requires additional dependencies, Windows-specific
    import_modules = [
        'debugpy', 'debugpy.adapter', 'debugpy.launcher', 'debugpy.server',
        'debugpy.common'
    ]

    version('1.4.1', sha256='889316de0b8ff3732927cb058cfbd3371e4cd0002ecc170d34c755ad289c867c')

    depends_on('python@2.7:2.8,3.5:', type=('build', 'link', 'run'))
    depends_on('py-setuptools', type='build')

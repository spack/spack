# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPyem(PythonPackage):
    """Project-level Python virtual environment management tool.

    PyEM manages multiple virtual environments local to projects.
    It provides shortcuts to create, remove, switch between, and run
    commands against virtual environments created against
    various Python interpreters."""

    homepage = "https://pypi.org/project/pyem/#description"
    pypi     = "pyem/pyem-2.1.0.tar.gz"

    version('2.1.0', sha256='5234a20427ab2813a8a0bf1e9112d4d854b1b0502b3e63d17c1b1a3c4be9340e')

    depends_on('python@3.7:', type=('build', 'run'))
    depends_on('py-virtualenv', type='build')
    depends_on('py-pip', type='build')
    depends_on('py-pytest', type=('build', 'run'))
    depends_on('py-mypy', type=('build', 'run'))
    depends_on('py-black', type=('build', 'run'))
    depends_on('flit', type=('build', 'run'))

    def install(self, spec, prefix):
        pip = which('pip')
        pip('install', self.stage.archive_file, '--prefix={0}'.format(prefix))


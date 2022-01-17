# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyCrashtest(PythonPackage):
    """Crashtest is a Python library that makes exceptions handling
    and inspection easier."""

    homepage = "https://github.com/sdispater/crashtest"
    pypi     = "crashtest/crashtest-0.3.1.tar.gz"

    version('0.3.1', sha256='42ca7b6ce88b6c7433e2ce47ea884e91ec93104a4b754998be498a8e6c3d37dd')

    depends_on('python@3.6:3', type=('build', 'run'))
    depends_on('py-poetry-core@1:', type='build')

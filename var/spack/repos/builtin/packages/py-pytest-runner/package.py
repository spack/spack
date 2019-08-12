# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPytestRunner(PythonPackage):
    """Invoke py.test as distutils command with dependency resolution."""

    homepage = "https://github.com/pytest-dev/pytest-runner"
    url      = "https://pypi.io/packages/source/p/pytest-runner/pytest-runner-2.11.1.tar.gz"

    import_modules = ['ptr']

    version('2.11.1', 'bdb73eb18eca2727944a2dcf963c5a81')

    depends_on('py-setuptools', type='build')
    depends_on('py-setuptools-scm@1.15:', type='build')

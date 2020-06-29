# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPathspec(PythonPackage):
    """pathspec extends the test loading and running features of unittest,
    making it easier to write, find and run tests."""

    homepage = "https://pypi.python.org/pypi/pathspec"
    url      = "https://pypi.io/packages/source/p/pathspec/pathspec-0.3.4.tar.gz"

    version('0.3.4', sha256='7605ca5c26f554766afe1d177164a2275a85bb803b76eba3428f422972f66728')

    depends_on('py-setuptools', type='build')

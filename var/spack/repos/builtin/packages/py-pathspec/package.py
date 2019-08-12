# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPathspec(PythonPackage):
    """pathspec extends the test loading and running features of unittest,
    making it easier to write, find and run tests."""

    homepage = "https://pypi.python.org/pypi/pathspec"
    url      = "https://pypi.io/packages/source/p/pathspec/pathspec-0.3.4.tar.gz"

    version('0.3.4', '2a4af9bf2dee98845d583ec61a00d05d')

    depends_on('py-setuptools', type='build')

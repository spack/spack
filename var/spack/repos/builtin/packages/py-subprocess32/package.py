# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PySubprocess32(PythonPackage):
    """A backport of the subprocess module from Python 3.2/3.3 for 2.x."""

    homepage = "https://pypi.python.org/pypi/subprocess32"
    url      = "https://pypi.io/packages/source/s/subprocess32/subprocess32-3.2.7.tar.gz"

    version('3.2.7', '824c801e479d3e916879aae3e9c15e16')

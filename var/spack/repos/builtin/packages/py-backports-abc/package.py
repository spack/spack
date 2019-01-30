# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyBackportsAbc(PythonPackage):
    """Backports_ABC: A backport of recent additions to the 'collections.abc'
    module."""
    homepage = "https://github.com/cython/backports_abc"
    url      = "https://github.com/cython/backports_abc/archive/0.4.tar.gz"

    version('0.4', 'e4246ae689221c9cbe84369fdb59e8c74d02b298')

    depends_on('py-setuptools', type='build')

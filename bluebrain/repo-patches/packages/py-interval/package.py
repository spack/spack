# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyInterval(PythonPackage):
    """Python interval and interval set implementation."""

    homepage = "https://pypi.org/project/interval/1.0.0/"
    url      = "https://pypi.io/packages/source/i/interval/interval-1.0.0.tar.bz2"

    version('1.0.0', sha256='6619937f3fcb5cf85bb3a60b4e4391664e8d7b30ae3dc4d04c3fc1d063ff1c3b')

    depends_on('python@:2', type=('build', 'run'))

# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyMacholib(PythonPackage):
    """Python package for Mach-O header analysis and editing"""

    pypi = "macholib/macholib-1.11.tar.gz"

    version('1.14', sha256='0c436bc847e7b1d9bda0560351bf76d7caf930fb585a828d13608839ef42c432')
    version('1.13', sha256='b71afea242d5ad4caacbdb79d80e75815d033fbc30f45954b2f3397f39683fd6')
    version('1.11', 'c4180ffc6f909bf8db6cd81cff4b6f601d575568f4d5dee148c830e9851eb9db')

    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('py-altgraph', type=('build', 'run'))

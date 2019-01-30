# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyEnum34(PythonPackage):
    """Python 3.4 Enum backported to 3.3, 3.2, 3.1, 2.7, 2.6, 2.5, and 2.4."""

    homepage = "https://pypi.python.org/pypi/enum34"
    url      = "https://pypi.io/packages/source/e/enum34/enum34-1.1.6.tar.gz"

    version('1.1.6', '5f13a0841a61f7fc295c514490d120d0')

    depends_on('python')
    conflicts('python@3.4:')

    # This dependency breaks concretization
    # See https://github.com/spack/spack/issues/2793
    # depends_on('py-ordereddict', when='^python@:2.6', type=('build', 'run'))
    depends_on('py-setuptools', type='build')

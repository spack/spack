# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyUnittest2(PythonPackage):
    """unittest2 is a backport of the new features added to the unittest
    testing framework in Python 2.7 and onwards."""

    homepage = "https://pypi.python.org/pypi/unittest2"
    url      = "https://pypi.io/packages/source/u/unittest2/unittest2-1.1.0.tar.gz"

    version('1.1.0', 'f72dae5d44f091df36b6b513305ea000')

    depends_on('py-setuptools', type='build')
    depends_on('py-enum34', when='^python@:3.3', type=('build', 'run'))
    depends_on('py-traceback2', type=('build', 'run'))
    depends_on('py-six', type=('build', 'run'))
    depends_on('py-argparse', type=('build', 'run'))

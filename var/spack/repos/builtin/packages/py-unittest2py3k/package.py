# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyUnittest2py3k(PythonPackage):
    """unittest2 is a backport of the new features added to the unittest
    testing framework in Python 2.7 and 3.2. This is a Python 3 compatible
    version of unittest2."""

    homepage = "https://pypi.python.org/pypi/unittest2py3k"
    url      = "https://pypi.io/packages/source/u/unittest2py3k/unittest2py3k-0.5.1.tar.gz"

    version('0.5.1', '8824ff92044310d9365f90d892bf0f09')

    depends_on('python@3:')
    depends_on('py-setuptools', type='build')

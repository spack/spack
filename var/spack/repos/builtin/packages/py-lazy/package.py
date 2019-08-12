# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyLazy(PythonPackage):
    """Lazy attributes for Python objects"""

    homepage = "https://pypi.python.org/pypi/lazy"
    url      = "https://pypi.io/packages/source/l/lazy/lazy-1.2.zip"

    version('1.2', '02713784e0a92ff9b6af1df8863dd79d')

    depends_on('py-setuptools', type='build')

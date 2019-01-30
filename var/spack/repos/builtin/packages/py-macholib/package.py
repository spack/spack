# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyMacholib(PythonPackage):
    """Python package for Mach-O header analysis and editing"""

    homepage = "https://pypi.python.org/pypi/macholib"
    url = "https://pypi.io/packages/source/m/macholib/macholib-1.8.tar.gz"

    version('1.8', '65af8f20dada7bdb2a142afbec51330e')

    depends_on('py-setuptools', type='build')

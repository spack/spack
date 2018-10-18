# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyWheel(PythonPackage):
    """A built-package format for Python."""

    homepage = "https://pypi.python.org/pypi/wheel"
    url      = "https://pypi.io/packages/source/w/wheel/wheel-0.29.0.tar.gz"

    version('0.29.0', '555a67e4507cedee23a0deb9651e452f')
    version('0.26.0', '4cfc6e7e3dc7377d0164914623922a10')

    depends_on('py-setuptools', type='build')

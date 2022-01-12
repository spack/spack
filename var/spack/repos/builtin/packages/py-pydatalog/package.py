# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPydatalog(PythonPackage):
    """pyDatalog adds logic programming to Python."""
    pypi = 'pyDatalog/pyDatalog-0.17.1.zip'

    version('0.17.1', sha256='b3d9cff0b9431e0fd0b2d5eefe4414c3d3c20bd18fdd7d1b42b2f01f25bac808')

    # pip silently replaces distutils with setuptools
    depends_on('py-setuptools', type='build')

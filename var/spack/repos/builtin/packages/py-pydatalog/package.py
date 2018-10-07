# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPydatalog(PythonPackage):
    """pyDatalog adds logic programming to Python."""
    homepage = 'https://pypi.python.org/pypi/pyDatalog/'
    url      = 'https://pypi.io/packages/source/p/pyDatalog/pyDatalog-0.17.1.zip'

    version('0.17.1', '6b2682301200068d208d6f2d01723939')

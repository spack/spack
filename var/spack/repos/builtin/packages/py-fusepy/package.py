# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyFusepy(PythonPackage):
    """Fusepy is a Python module that provides a simple interface to FUSE and
    MacFUSE. It's just one file and is implemented using ctypes."""

    homepage = "https://github.com/fusepy/fusepy"
    url      = "https://github.com/fusepy/fusepy/archive/v2.0.4.tar.gz"

    version('2.0.4', '0b0bf1283d6fe9532ecbf6c8204f05d3')

    depends_on('py-setuptools', type='build')

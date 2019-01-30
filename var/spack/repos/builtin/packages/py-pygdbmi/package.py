# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPygdbmi(PythonPackage):
    """Parse gdb machine interface output with Python"""

    homepage = "https://github.com/cs01/pygdbmi"
    url      = "https://pypi.io/packages/source/p/pygdbmi/pygdbmi-0.8.2.0.tar.gz"

    version('0.8.2.0', 'e74d3d02fa5eef1223b5dedb13f9bbad')

    depends_on('py-setuptools', type='build')

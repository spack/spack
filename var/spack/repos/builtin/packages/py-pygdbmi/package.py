# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPygdbmi(PythonPackage):
    """Parse gdb machine interface output with Python"""

    homepage = "https://github.com/cs01/pygdbmi"
    url      = "https://pypi.io/packages/source/p/pygdbmi/pygdbmi-0.8.2.0.tar.gz"

    version('0.8.2.0', sha256='47cece65808ca42edf6966ac48e2aedca7ae1c675c4d2f0d001c7f3a7fa245fe')

    depends_on('py-setuptools', type='build')

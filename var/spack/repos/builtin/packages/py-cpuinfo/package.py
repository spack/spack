# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyCpuinfo(PythonPackage):
    """Get CPU info with pure Python 2 & 3"""

    homepage = "https://github.com/workhorsy/py-cpuinfo"
    url      = "https://pypi.io/packages/source/p/py-cpuinfo/py-cpuinfo-0.2.3.tar.gz"

    version('0.2.3', '780ff46a0e122af09cb2c40b2706c6dc')

    depends_on('py-setuptools', type='build')

# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

#
from spack import *


class PyIpaddress(PythonPackage):
    """Python 3.3's ipaddress for older Python versions"""

    homepage = "https://github.com/phihag/ipaddress"
    url      = "https://pypi.io/packages/source/i/ipaddress/ipaddress-1.0.18.tar.gz"

    version('1.0.18', '310c2dfd64eb6f0df44aa8c59f2334a7')

    depends_on('py-setuptools', type='build')

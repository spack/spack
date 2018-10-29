# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Tinyxml2(CMakePackage):
    """Simple, small, efficient, C++ XML parser"""

    homepage = "http://grinninglizard.com/tinyxml2/"
    url = "https://github.com/leethomason/tinyxml2/archive/3.0.0.tar.gz"

    version('4.0.1', '08570d385788f6b02f50f5fd9df32a9d4f8482cc')
    version('4.0.0', '7a6f0858d75f360922f3ca272f7067e8cdf00489')
    version('3.0.0', '07acaae49f7dd3dab790da4fe72d0c7ef0d116d1')
    version('2.2.0', '7869aa08241ce16f93ba3732c1cde155b1f2b6a0')
    version('2.1.0', '70ef3221bdc190fd8fc50cdd4a6ef440f44b74dc')
    version('2.0.2', 'c78a4de58540e2a35f4775fd3e577299ebd15117')

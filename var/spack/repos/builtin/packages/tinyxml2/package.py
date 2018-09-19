##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
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

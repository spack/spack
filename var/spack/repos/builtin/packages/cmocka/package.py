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


class Cmocka(CMakePackage):
    """Unit-testing framework in pure C"""
    homepage = "https://cmocka.org/"
    url      = "https://cmocka.org/files/1.1/cmocka-1.1.1.tar.xz"

    version('1.1.1', '6fbff4e42589566eda558db98b97623e')
    version('1.1.0', '59c9aa5735d9387fb591925ec53523ec')
    version('1.0.1', 'ed861e501a21a92b2af63e466df2015e')

    depends_on('cmake@2.6.0:', type='build')

    parallel = False

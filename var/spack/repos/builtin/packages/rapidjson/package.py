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


class Rapidjson(CMakePackage):
    """A fast JSON parser/generator for C++ with both SAX/DOM style API"""

    homepage = "http://rapidjson.org"
    url      = "https://github.com/Tencent/rapidjson/archive/v1.1.0.tar.gz"

    version('1.1.0', 'badd12c511e081fec6c89c43a7027bce')
    version('1.0.2', '97cc60d01282a968474c97f60714828c')
    version('1.0.1', '48cc188df49617b859d13d31344a50b8')
    version('1.0.0', '08247fbfa464d7f15304285f04b4b228')

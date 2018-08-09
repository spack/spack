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


class Xtl(CMakePackage):
    """QuantStack tools library"""

    homepage = "https://github.com/QuantStack/xtl"
    url      = "https://github.com/QuantStack/xtl/archive/0.3.4.tar.gz"
    git      = "https://github.com/QuantStack/xtl.git"

    maintainers = ['ax3l']

    version('develop', branch='master')
    version('0.4.0', '48c76b63ab12e497a53fb147c41ae747')
    version('0.3.4', 'b76548a55f1e171a9c849e5ed543e8b3')
    version('0.3.3', '09b6d9611e460d9280bf1156bcca20f5')

    # C++14 support
    conflicts('%gcc@:4.8')
    conflicts('%clang@:3.6')
    # untested: conflicts('%intel@:15')
    # untested: conflicts('%pgi@:14')

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


class Spglib(CMakePackage):
    """C library for finding and handling crystal symmetries."""

    homepage = "https://atztogo.github.io/spglib/"
    url      = "https://github.com/atztogo/spglib/archive/v1.10.3.tar.gz"

    patch('fix_cmake_install.patch', when='@:1.10.3')
    # patch by Krishnendu Ghosh
    patch('fix_cpp.patch', when='@:1.10.3')

    version('1.10.3', 'f6ef0554fa528ffa49d8eaee18a2b7b9')
    version('1.10.0', '0ad9330ae8a511d25e2e26cb9bf02808')

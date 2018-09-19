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


class Typhon(CMakePackage):
    """
    Typhon is a distributed communications library for unstructured mesh
    applications.
    """

    homepage = "https://github.com/UK-MAC/Typhon"
    url      = "https://github.com/UK-MAC/Typhon/archive/v3.0.tar.gz"
    git      = "https://github.com/UK-MAC/Typhon.git"

    version('develop', branch='develop')

    version('3.0.1', '89045decfba5fd468ef05ad4c924df8c')
    version('3.0', 'ec67cd1aa585ce2410d4fa50514a916f')

    depends_on('mpi')

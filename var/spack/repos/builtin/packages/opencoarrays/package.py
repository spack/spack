##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
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


class Opencoarrays(CMakePackage):
    """OpenCoarrays is an open-source software project that produces an
    application binary interface (ABI) supporting coarray Fortran (CAF)
    compilers, an application programming interface (API) that supports users
    of non-CAF compilers, and an associated compiler wrapper and program
    launcher.
    """

    homepage = "http://www.opencoarrays.org/"
    url      = "https://github.com/sourceryinstitute/opencoarrays/releases/download/1.7.4/OpenCoarrays-1.7.4.tar.gz"

    version('1.7.4', '85ba87def461e3ff5a164de2e6482930')
    version('1.6.2', '5a4da993794f3e04ea7855a6678981ba')

    depends_on('cmake', type='build')
    depends_on('mpi')

    provides('coarrays')

    def cmake_args(self):
        args = []
        args.append("-DCMAKE_C_COMPILER=%s" % self.spec['mpi'].mpicc)
        args.append("-DCMAKE_Fortran_COMPILER=%s" % self.spec['mpi'].mpifc)
        return args

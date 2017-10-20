##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
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


class Amrex(AutotoolsPackage):
    """AMReX is the successor to BoxLib.
       It is a Block-Structured AMR Framework.
    """

    homepage = "https://ccse.lbl.gov/AMReX/index.html"
    url      = "https://github.com/AMReX-Codes/amrex.git"

    version('17.06', git='https://github.com/AMReX-Codes/amrex.git', commit='836d3c7')
    version('master', git='https://github.com/AMReX-Codes/amrex.git', tag='master')
    version('develop', git='https://github.com/AMReX-Codes/amrex.git', tag='development')

    variant('dims',
        default='3',
        values=('1', '2', '3'),
        multi=False,
        description='Number of spatial dimensions')

    variant('mpi', default=True, description='Enable MPI parallel support')

    depends_on('mpi', when='+mpi')

    def configure_args(self):
        spec = self.spec

        extra_args = ['--dim=%d' % int(spec.variants['dims'].value)]

        return extra_args

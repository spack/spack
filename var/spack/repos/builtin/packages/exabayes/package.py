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


class Exabayes(AutotoolsPackage):
    """ExaBayes is a software package for Bayesian tree inference. It is
       particularly suitable for large-scale analyses on computer clusters."""

    homepage = "https://sco.h-its.org/exelixis/web/software/exabayes/"
    url      = "https://sco.h-its.org/exelixis/resource/download/software/exabayes-1.5.tar.gz"

    version('1.5', '6a734777b8f8eff0a520306500c8c419')

    variant('mpi', default=True, description='Enable MPI parallel support')

    depends_on('mpi', when='+mpi')

    # ExaBayes manual states the program succesfully compiles with GCC, version
    # 4.6 or greater, and Clang, version 3.2 or greater. The build fails when
    # GCC 7.1.0 is used.
    conflicts('%gcc@:4.5.4, 7.1.0:')
    conflicts('%clang@:3.1')
    conflicts('^intel-mpi', when='+mpi')
    conflicts('^intel-parallel-studio+mpi', when='+mpi')
    conflicts('^mvapich2', when='+mpi')
    conflicts('^spectrum-mpi', when='+mpi')

    def configure_args(self):
        args = []
        if '+mpi' in self.spec:
            args.append('--enable-mpi')
        else:
            args.append('--disable-mpi')
        return args

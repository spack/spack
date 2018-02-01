##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
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
import os
import sys


class Mpip(AutotoolsPackage):
    """mpiP: Lightweight, Scalable MPI Profiling"""
    homepage = "http://mpip.sourceforge.net/"
    url      = "http://downloads.sourceforge.net/project/mpip/mpiP/mpiP-3.4.1/mpiP-3.4.1.tar.gz"

    version("3.4.1", "1168adc83777ac31d6ebd385823aabbd")

    depends_on("libelf")
    depends_on("libdwarf")
    # darwin has libunwind installed, and building GNU libunwind
    # doesn't work on darwin right now
    depends_on('libunwind',
               when=(os.uname()[4] == "x86_64" and sys.platform != 'darwin'))
    depends_on("mpi")
    depends_on('binutils')

    parallel = False

    # malloc.h doesn't need to be included; stdlib.h suffices
    patch('malloc.h.patch')

    # bfd.h requires some macros to be defined in advance
    # see https://github.com/mlpack/mlpack/pull/575
    patch('bfd.patch')

    def configure_args(self):
        config_args = ['--without-f77']
        config_args.append('--enable-libunwind')
        config_args.append('--enable-bfd')
        config_args.append("--with-cc=%s" % self.spec['mpi'].mpicc)
        config_args.append("--with-cxx=%s" % self.spec['mpi'].mpicxx)

        return config_args

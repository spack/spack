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


class RRmpi(RPackage):
    """An interface (wrapper) to MPI APIs. It also provides interactive R
       manager and worker environment."""

    homepage = "http://www.stats.uwo.ca/faculty/yu/Rmpi"
    url      = "https://cran.r-project.org/src/contrib/Rmpi_0.6-6.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/Rmpi"

    version('0.6-6', '59ae8ce62ff0ff99342d53942c745779')

    depends_on('mpi')
    depends_on('r@2.15.1:')

    def install(self, spec, prefix):
        if 'mpich' in spec:
            Rmpi_type = 'MPICH'
        elif 'mvapich' in spec:
            Rmpi_type = 'MVAPICH'
        else:
            Rmpi_type = 'OPENMPI'

        my_mpi = spec['mpi']

        R('CMD', 'INSTALL',
          '--configure-args=--with-Rmpi-type=%s' % Rmpi_type +
          ' --with-mpi=%s' % my_mpi.prefix,
          '--library={0}'.format(self.module.r_lib_dir),
          self.stage.source_path)

##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
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


class Nekbone(Package):
    """NEK5000 emulation software called NEKbone. Nekbone captures the basic
       structure and user interface of the extensive Nek5000 software.
       Nek5000 is a high order, incompressible Navier-Stokes solver based on
       the spectral element method."""

    homepage = "https://github.com/ANL-CESAR/"
    url = "https://github.com/ANL-CESAR/nekbone.git"

    tags = ['proxy-app']

    version('develop', git='https://github.com/ANL-CESAR/nekbone.git')

    depends_on('mpi')

    def install(self, spec, prefix):

        working_dirs = ['example1', 'example2', 'example3', 'nek_comm',
                        'nek_delay', 'nek_mgrid']
        mkdir(prefix.bin)

        for wdir in working_dirs:
            with working_dir('test/' + wdir):
                makenec = FileFilter('makenek')
                makenec.filter('CC.*', 'CC=' + self.spec['mpi'].mpicc)
                makenec.filter('FF77.*', 'FF77=' + self.spec['mpi'].mpif77)
                makenek = Executable('./makenek')
                path = join_path(prefix.bin,  wdir)
                makenek('ex1', '../../src')
                mkdir(path)
                install('nekbone', path)
                install('nekpmpi', path)

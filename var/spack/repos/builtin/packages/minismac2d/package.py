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


class Minismac2d(MakefilePackage):
    """Proxy Application. Solves the finite-differenced 2D incompressible
       Navier-Stokes equations with Spalart-Allmaras one-equation
       turbulence model on a structured body conforming grid.
    """

    homepage = "http://mantevo.org"
    url      = "http://mantevo.org/downloads/releaseTarballs/miniapps/MiniSMAC2D/miniSMAC2D-2.0.tgz"

    tags = ['proxy-app']

    version('2.0', '1bb1a52cea21bc9162bf7a71a6ddf37d')

    depends_on('mpi')

    parallel = False

    @property
    def build_targets(self):
        targets = [
            'CPP=cpp',
            'FC={0}'.format(self.spec['mpi'].mpifc),
            'LD={0}'.format(self.spec['mpi'].mpifc),
            'MPIDIR=-I{0}'.format(self.spec['mpi'].headers.directories[0]),
            'CPPFLAGS=-P -traditional  -DD_PRECISION',
            'FFLAGS=-O3 -c -g -DD_PRECISION',
            'LDFLAGS=-O3',
            '--file=Makefile_mpi_only'
        ]

        return targets

    def edit(self, spec, prefix):
        # Editing input file to point to installed data files
        param_file = FileFilter('smac2d.in')
        param_file.filter('bcmain_directory=.*', "bcmain_directory='.'")
        param_file.filter('bcmain_filename=.*',
                          "bcmain_filename='bcmain.dat_original_119x31'")
        param_file.filter('xygrid_directory=.*', "xygrid_directory='.'")
        param_file.filter('xygrid_filename=.*',
                          "xygrid_filename='xy.dat_original_119x31'")

    def install(self, spec, prefix):
        # Manual Installation
        mkdirp(prefix.bin)
        mkdirp(prefix.doc)

        install('smac2d_mpi_only', prefix.bin)
        install('bcmain.dat_original_119x31', prefix.bin)
        install('xy.dat_original_119x31', prefix.bin)
        install('smac2d.in', prefix.bin)
        install('README.txt', prefix.doc)

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


class Nekcem(Package):
    """Spectral-element solver for Maxwell's equations, drift-diffusion
       equations, and more."""

    # Links to homepage and git
    homepage = "https://nekcem.mcs.anl.gov"
    url      = "https://github.com/NekCEM/NekCEM/archive/development.zip"

    # Variants
    variant('mpi', default=True, description='Build with MPI')

    # We only have a development version
    version('develop', git='https://github.com/NekCEM/NekCEM.git')

    # dependencies
    depends_on('mpi', when='+mpi')
    depends_on('python@2.7:')
    depends_on('blas')
    depends_on('lapack')

    @run_before('install')
    def fortran_check(self):
        if not self.compiler.fc:
            msg = 'NekCEM can not be built without a Fortran compiler.'
            raise RuntimeError(msg)

    def install(self, spec, prefix):
        binDir = 'bin'
        nek = 'nek'
        cNek = 'configurenek'
        mNek = 'makenek'

        FC = self.compiler.fc
        CC = self.compiler.cc

        if '+mpi' in spec:
            FC = spec['mpi'].mpif77
            CC = spec['mpi'].mpicc

        with working_dir(binDir):
            filter_file(r'^FC\s*=.*', 'FC=\"' + FC + '\"', 'makenek')
            filter_file(r'^CC\s*=.*', 'CC=\"' + CC + '\"', 'makenek')
            filter_file(r'^NEK\s*=.*', 'NEK=\"' + prefix.bin.NekCEM +
                        '\"', 'makenek')

            blasLapack = spec['lapack'].libs + spec['blas'].libs
            ldFlags = blasLapack.ld_flags
            # Temporary workaround, we should use LDFLAGS when
            # configurenek in Nekcem is fixed.
            # See issue: https://github.com/NekCEM/NekCEM/issues/200
            filter_file(r'^EXTRALDFLAGS\s*=.*', 'EXTRALDFLAGS=\"' + ldFlags +
                        '\"', 'makenek')

        # Install NekCEM in prefix/bin
        install_tree('../NekCEM', prefix.bin.NekCEM)
        # Create symlinks to makenek, nek and configurenek scripts
        os.symlink(os.path.join(prefix.bin.NekCEM, binDir, mNek),
                   os.path.join(prefix.bin, mNek))
        os.symlink(os.path.join(prefix.bin.NekCEM, binDir, cNek),
                   os.path.join(prefix.bin, cNek))
        os.symlink(os.path.join(prefix.bin.NekCEM, binDir, nek),
                   os.path.join(prefix.bin, nek))

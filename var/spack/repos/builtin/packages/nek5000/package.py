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

import numbers


def is_integral(x):
    """Any integer value"""
    try:
        return isinstance(int(x), numbers.Integral) and \
            not isinstance(x, bool) and int(x) > 0
    except ValueError:
        return False


class Nek5000(Package):
    """A fast and scalable high-order solver for computational fluid
       dynamics"""

    homepage = "https://nek5000.mcs.anl.gov/"
    url      = "https://github.com/Nek5000/Nek5000"

    tags = ['cfd', 'flow', 'hpc', 'solver', 'navier-stokes',
            'spectral-elements', 'fluid']

    version('17.0.0-beta2', git='https://github.com/Nek5000/Nek5000.git',
        commit='b95f46c59f017fff2fc19b66aa65a881085a7572')
    version('develop',      git='https://github.com/Nek5000/Nek5000.git',
        branch='master')

    # MPI, Profiling and Visit variants
    variant('mpi',       default=True, description='Build with MPI.')
    variant('profiling', default=True, description='Build with profiling data.')
    variant('visit',     default=False, description='Build with Visit.')

    # Variant for MAXNEL, we need to read this from user
    variant(
        'MAXNEL',
        default=150000,
        description='Maximum number of elements for Nek5000 tools.',
        values=is_integral
    )

    # Variants for Nek tools
    variant('genbox',   default=True, description='Build genbox tool.')
    variant('int_tp',   default=True, description='Build int_tp tool.')
    variant('n2to3',    default=True, description='Build n2to3 tool.')
    variant('postnek',  default=True, description='Build postnek tool.')
    variant('reatore2', default=True, description='Build reatore2 tool.')
    variant('genmap',   default=True, description='Build genmap tool.')
    variant('nekmerge', default=True, description='Build nekmerge tool.')
    variant('prenek',   default=True, description='Build prenek tool.')

    # Dependencies
    depends_on('mpi', when="+mpi")
    depends_on('visit', when="+visit")

    @run_before('install')
    def fortran_check(self):
        if not self.compiler.fc:
            msg = 'Cannot build Nek5000 without a Fortran compiler.'
            raise RuntimeError(msg)

    def install(self, spec, prefix):
        toolsDir   = 'tools'
        binDir     = 'bin'

        F77 = self.compiler.fc
        CC  = self.compiler.cc

        # Build the tools, maketools copy them to Nek5000/bin by default.
        # We will then install Nek5000/bin under prefix after that.
        with working_dir(toolsDir):
            # Update the maketools script to use correct compilers
            if self.version == Version('17.0.0-beta2'):  # Old release
                filter_file(r'^F77\s*=.*', 'F77=\"' + F77 + '\"', 'maketools')
            else:
                filter_file(r'^FC\s*=.*', 'FC=\"' + F77 + '\"', 'maketools')
            filter_file(r'^CC\s*=.*', 'CC=\"' + CC  + '\"',   'maketools')

            maxnel = self.spec.variants['MAXNEL'].value
            filter_file(r'^#MAXNEL\s*=.*', 'MAXNEL=' + maxnel, 'maketools')

            makeTools = Executable('./maketools')

            # Build the tools
            if '+genbox' in spec:
                makeTools('genbox')
            if '+int_tp' in spec and self.version == Version('17.0.0-beta2'):
                makeTools('int_tp')
            if '+n2to3' in spec:
                makeTools('n2to3')
            if '+postnek' in spec:
                makeTools('postnek')
            if '+reatore2' in spec:
                makeTools('reatore2')
            if '+genmap' in spec:
                makeTools('genmap')
            if '+nekmerge' in spec:
                makeTools('nekmerge')
            if '+prenek' in spec:
                makeTools('prenek')

        with working_dir(binDir):
            if '+mpi' in spec:
                F77 = spec['mpi'].mpif77
                CC  = spec['mpi'].mpicc
            else:
                filter_file(r'^#MPI=0', 'MPI=0', 'makenek')

            if '+profiling' not in spec:
                filter_file(r'^#PROFILING=0', 'PROFILING=0', 'makenek')

            if '+visit' in spec:
                filter_file(r'^#VISIT=1', 'VISIT=1', 'makenek')
                filter_file(r'^#VISIT_INSTALL=.*', 'VISIT_INSTALL=\"' +
                            spec['visit'].prefix.bin + '\"', 'makenek')

            # Update the makenek to use correct compilers and
            # Nek5000 source.
            filter_file(r'^F77\s*=.*', 'F77=\"' + F77 + '\"', 'makenek')
            filter_file(r'^CC\s*=.*', 'CC=\"'  + CC  + '\"',  'makenek')
            filter_file(r'SOURCE_ROOT\s*=\"\$H.*',  'SOURCE_ROOT=\"' +
                        prefix.bin.Nek5000 + '\"',  'makenek')

        # Install Nek5000/bin in prefix/bin
        install_tree(binDir, prefix.bin)

        # Copy Nek5000 source to prefix/bin
        install_tree('../Nek5000', prefix.bin.Nek5000)

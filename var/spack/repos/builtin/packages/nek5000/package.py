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

import numbers
import os


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
    url      = "https://github.com/Nek5000/Nek5000/releases/download/v17.0/Nek5000-v17.0.tar.gz"
    git      = "https://github.com/Nek5000/Nek5000.git"

    tags = ['cfd', 'flow', 'hpc', 'solver', 'navier-stokes',
            'spectral-elements', 'fluid', 'ecp', 'ecp-apps']

    version('develop', branch='master')
    version('17.0', '6a13bfad2ce023897010dd88f54a0a87')

    # MPI, Profiling and Visit variants
    variant('mpi',       default=True, description='Build with MPI.')
    variant('profiling', default=True, description='Build with profiling data.')
    variant('visit',     default=False, description='Build with Visit.')

    # TODO: add a variant 'blas' or 'external-blas' to enable the usage of
    #       Spack installed/configured blas.

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
    depends_on('libx11', when="+prenek")
    depends_on('libx11', when="+postnek")
    # libxt is needed for X11/Intrinsic.h but not for linking
    depends_on('libxt', when="+prenek")
    depends_on('xproto', when="+prenek")
    depends_on('libxt', when="+postnek")
    depends_on('visit', when="+visit")

    @run_before('install')
    def fortran_check(self):
        if not self.compiler.f77:
            msg = 'Cannot build Nek5000 without a Fortran 77 compiler.'
            raise RuntimeError(msg)

    @run_after('install')
    def test_install(self):
        with working_dir('short_tests/eddy'):
            os.system(join_path(self.prefix.bin, 'makenek') + ' eddy_uv')
            if not os.path.isfile(join_path(os.getcwd(), 'nek5000')):
                msg = 'Cannot build example: short_tests/eddy.'
                raise RuntimeError(msg)

    def install(self, spec, prefix):
        tools_dir   = 'tools'
        bin_dir     = 'bin'

        # Do not use the Spack compiler wrappers.
        # Use directly the compilers:
        fc  = self.compiler.f77
        cc  = self.compiler.cc

        fflags = spec.compiler_flags['fflags']
        cflags = spec.compiler_flags['cflags']
        if ('+prenek' in spec) or ('+postnek' in spec):
            libx11_h = find_headers('Xlib', spec['libx11'].prefix.include,
                                    recursive=True)
            if not libx11_h:
                raise RuntimeError('Xlib.h not found in %s' %
                                   spec['libx11'].prefix.include)
            cflags += ['-I%s' % os.path.dirname(libx11_h.directories[0])]

            xproto_h = find_headers('X', spec['xproto'].prefix.include,
                                    recursive=True)
            if not xproto_h:
                raise RuntimeError('X.h not found in %s' %
                                   spec['xproto'].prefix.include)
            cflags += ['-I%s' % os.path.dirname(xproto_h.directories[0])]

            libxt_h = find_headers('Intrinsic', spec['libxt'].prefix.include,
                                   recursive=True)
            if not libxt_h:
                raise RuntimeError('X11/Intrinsic.h not found in %s' %
                                   spec['libxt'].prefix.include)
            cflags += ['-I%s' % os.path.dirname(libxt_h.directories[0])]
        if self.compiler.name in ['xl', 'xl_r']:
            # Use '-qextname' to add underscores.
            # Use '-WF,-qnotrigraph' to fix an error about a string: '... ??'
            fflags += ['-qextname', '-WF,-qnotrigraph']
        fflags = ' '.join(fflags)
        cflags = ' '.join(cflags)

        # Build the tools, maketools copy them to Nek5000/bin by default.
        # We will then install Nek5000/bin under prefix after that.
        with working_dir(tools_dir):
            # Update the maketools script to use correct compilers
            filter_file(r'^#FC\s*=.*', 'FC="{0}"'.format(fc), 'maketools')
            filter_file(r'^#CC\s*=.*', 'CC="{0}"'.format(cc), 'maketools')
            if fflags:
                filter_file(r'^#FFLAGS=.*', 'FFLAGS="{0}"'.format(fflags),
                            'maketools')
            if cflags:
                filter_file(r'^#CFLAGS=.*', 'CFLAGS="{0}"'.format(cflags),
                            'maketools')

            if self.compiler.name in ['xl', 'xl_r']:
                # Patch 'maketools' to use '-qextname' when checking for
                # underscore becasue 'xl'/'xl_r' use this option to enable the
                # addition of the underscore.
                filter_file(r'^\$FC -c ', '$FC -qextname -c ', 'maketools')

            libx11_lib = find_libraries('libX11', spec['libx11'].prefix.lib,
                                        shared=True, recursive=True)
            if not libx11_lib:
                libx11_lib = \
                    find_libraries('libX11', spec['libx11'].prefix.lib64,
                                   shared=True, recursive=True)
            if not libx11_lib:
                raise RuntimeError('libX11 not found in %s/{lib,lib64}' %
                                   spec['libx11'].prefix)
            # There is no other way to set the X11 library path except brute
            # force:
            filter_file(r'-L\$\(X\)', libx11_lib.search_flags,
                        join_path('prenek', 'makefile'))
            filter_file(r'-L\$\(X\)', libx11_lib.search_flags,
                        join_path('postnek', 'makefile'))

            if self.compiler.name in ['xl', 'xl_r']:
                # Use '-qextname' when compiling mxm.f
                filter_file('\$\(OLAGS\)', '-qextname $(OLAGS)',
                            join_path('postnek', 'makefile'))
            # Define 'rename_' function that calls 'rename'
            with open(join_path('postnek', 'xdriver.c'), 'a') as xdriver:
                xdriver.write('\nvoid rename_(char *from, char *to)\n{\n'
                              '   rename(from, to);\n}\n')

            maxnel = self.spec.variants['MAXNEL'].value
            filter_file(r'^#MAXNEL\s*=.*', 'MAXNEL=' + maxnel, 'maketools')

            maketools = Executable('./maketools')

            # Build the tools
            if '+genbox' in spec:
                maketools('genbox')
            # "ERROR: int_tp does not exist!"
            # if '+int_tp' in spec:
            #     maketools('int_tp')
            if '+n2to3' in spec:
                maketools('n2to3')
            if '+postnek' in spec:
                maketools('postnek')
            if '+reatore2' in spec:
                maketools('reatore2')
            if '+genmap' in spec:
                maketools('genmap')
            if '+nekmerge' in spec:
                maketools('nekmerge')
            if '+prenek' in spec:
                maketools('prenek')

        with working_dir(bin_dir):
            if '+mpi' in spec:
                fc  = spec['mpi'].mpif77
                cc  = spec['mpi'].mpicc
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
            filter_file(r'^#FC\s*=.*', 'FC="{0}"'.format(fc), 'makenek')
            filter_file(r'^#CC\s*=.*', 'CC="{0}"'.format(cc), 'makenek')
            filter_file(r'^#SOURCE_ROOT\s*=\"\$H.*',  'SOURCE_ROOT=\"' +
                        prefix.bin.Nek5000 + '\"',  'makenek')
            if fflags:
                filter_file(r'^#FFLAGS=.*', 'FFLAGS="{0}"'.format(fflags),
                            'makenek')
            if cflags:
                filter_file(r'^#CFLAGS=.*', 'CFLAGS="{0}"'.format(cflags),
                            'makenek')

        with working_dir('core'):
            if self.compiler.name in ['xl', 'xl_r']:
                # Patch 'core/makenek.inc' and 'makefile.template' to use
                # '-qextname' when checking for underscore becasue 'xl'/'xl_r'
                # use this option to enable the addition of the underscore.
                filter_file(r'^\$FCcomp -c ', '$FCcomp -qextname -c ',
                            'makenek.inc')
                filter_file(r'\$\(FC\) -c \$\(L0\)',
                            '$(FC) -c -qextname $(L0)', 'makefile.template')

        # Install Nek5000/bin in prefix/bin
        install_tree(bin_dir, prefix.bin)

        # Copy Nek5000 source to prefix/bin
        install_tree('../Nek5000', prefix.bin.Nek5000)

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
import glob
import os


class SuperluMt(Package):
    """SuperLU is a general purpose library for the direct solution of large,
    sparse, nonsymmetric systems of linear equations on high performance
    machines. SuperLU_MT is designed for shared memory parallel machines."""

    homepage = "http://crd-legacy.lbl.gov/~xiaoye/SuperLU/#superlu_mt"
    url      = "http://crd-legacy.lbl.gov/~xiaoye/SuperLU/superlu_mt_3.1.tar.gz"

    version('3.1', '06ac62f1b4b7d17123fffa0d0c315e91')

    variant('blas',    default=True,
            description='Build with external BLAS library')

    # Must choose one or the other
    variant('openmp',  default=False, description='Build with OpenMP support')
    variant('pthread', default=True,
            description='Build with POSIX threads support')

    # NOTE: must link with a single-threaded BLAS library
    depends_on('blas', when='+blas')

    # Cannot be built in parallel
    parallel = False

    def configure(self, spec):
        # Validate chosen variants
        if '+openmp' in spec and '+pthread' in spec:
            msg = 'You cannot choose both +openmp and +pthread'
            raise RuntimeError(msg)
        if '~openmp' in spec and '~pthread' in spec:
            msg = 'You must choose either +openmp or +pthread'
            raise RuntimeError(msg)

        # List of configuration options
        config = []

        # The machine (platform) identifier to append to the library names
        if '+openmp' in spec:
            # OpenMP
            config.extend([
                'PLAT       = _OPENMP',
                'TMGLIB     = libtmglib.a',
                'MPLIB      = {0}'.format(self.compiler.openmp_flag),
                'CFLAGS     = {0}'.format(self.compiler.openmp_flag),
                'FFLAGS     = {0}'.format(self.compiler.openmp_flag)
            ])
        elif '+pthread' in spec:
            # POSIX threads
            config.extend([
                'PLAT       = _PTHREAD',
                'TMGLIB     = libtmglib$(PLAT).a',
                'MPLIB      = -lpthread'
            ])

        # The BLAS library
        # NOTE: must link with a single-threaded BLAS library
        if '+blas' in spec:
            config.extend([
                'BLASDEF    = -DUSE_VENDOR_BLAS',
                'BLASLIB    = {0}'.format(spec['blas'].libs.ld_flags)
            ])
        else:
            config.append('BLASLIB    = ../lib/libblas$(PLAT).a')

        # Generic options
        config.extend([
            # The name of the libraries to be created/linked to
            'SUPERLULIB = libsuperlu_mt$(PLAT).a',
            'MATHLIB    = -lm',
            # The archiver and the flag(s) to use when building archives
            'ARCH       = ar',
            'ARCHFLAGS  = cr',
            'RANLIB     = {0}'.format('ranlib' if which('ranlib') else 'echo'),
            # Definitions used by CPP
            'PREDEFS    = -D_$(PLAT)',
            # Compilers and flags
            'CC         = {0}'.format(os.environ['CC']),
            'CFLAGS    += $(PREDEFS) -D_LONGINT',
            'NOOPTS     = -O0',
            'FORTRAN    = {0}'.format(os.environ['FC']),
            'LOADER     = {0}'.format(os.environ['CC']),
            # C preprocessor defs for compilation
            'CDEFS      = -DAdd_'
        ])

        # Write configuration options to include file
        with open('make.inc', 'w') as inc:
            for option in config:
                inc.write('{0}\n'.format(option))

    def install(self, spec, prefix):
        # Set up make include file manually
        self.configure(spec)

        # BLAS needs to be compiled separately if using internal BLAS library
        if '+blas' not in spec:
            make('blaslib')

        make()

        # Install manually
        install_tree('lib', prefix.lib)

        headers = glob.glob(join_path('SRC', '*.h'))
        mkdir(prefix.include)
        for h in headers:
            install(h, prefix.include)

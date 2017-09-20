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
from distutils.dir_util import copy_tree


class Cpmd(Package):
    """The CPMD code is a parallelized plane wave / pseudopotential
       implementation of Density Functional Theory, particularly designed
       for ab-initio molecular dynamics.
    """

    homepage = "http://www.cpmd.org/"
    url      = "cpmd-v4.1.tar.gz"

    version('v4.1', 'f70aedefa2e5f8a5f8d79afdd99d0895')

    variant('openmp', default=False, description='Enables openMP support')

    depends_on('mpi')
    depends_on('blas')
    depends_on('lapack')
    depends_on('fftw', when='~openmp')
    depends_on('fftw+openmp', when='+openmp')

    def install(self, spec, prefix):
        bash = which('bash')

        if '%intel' in self.spec:
            architecture = 'LINUX-X86_64-INTEL-MPI'
            filter_file('mpicc', spec['mpi'].mpicc, 'configure/%s'
                        % architecture)
            filter_file('mpif90', spec['mpi'].mpifc, 'configure/%s'
                        % architecture)
            filter_file('(CPP=)(\')(.+)(\')', r'\1\2\%s\4' %
                        'fpp -P', 'configure/%s' % architecture)

        elif '%gcc' in self.spec:
            architecture = 'LINUX-I686-FEDORA-MPI-FFTW'
            # by default CPMD use FFTW when compiled with gnu
            # It's better FFTW3
            filter_file('(CPPFLAGS=)(\')(.+)(\')', r'\1\2\3%s\4' %
                        ' -D__HAS_FFT_FFTW3', 'configure/%s' % architecture)
            # the option -ffree-line-length-none is necessary to avoid
            # errors occurring when a line is too long
            filter_file('(FFLAGS=)(\')(.+)(\')', r'\1\2\3%s\4' %
                        ' -ffree-line-length-none', 'configure/%s' %
                        architecture)

            libs = ''
            libs += str(spec['blas'].libs)
            if '+openmp' in spec:
                string = spec['fftw'].prefix.lib
                fftwlib = ' -L%s' % string + ' -lfftw3_omp -lfftw3'
            else:
                string = spec['fftw'].prefix.lib
                fftwlib = ' -L%s' % string + ' -lfftw3'
            libs += fftwlib
            filter_file('(LIBS=)(\')(.+)(\')', r'\1\2%s\4' % libs,
                        'configure/%s' % architecture)

        if '+openmp' in spec:
            bash('-c', 'export omp=1;./configure.sh %s' % architecture)
        else:
            bash('-c', './configure.sh %s' % architecture)

        make(parallel=False)
        copy_tree('bin', self.prefix.bin)

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
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install qmcpack
#
# You can edit this file again by typing:
#
#     spack edit qmcpack
#
# See the Spack documentation for more information on packaging.
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
from spack import *


class Qmcpack(CMakePackage):
    """QMCPACK, is a modern high-performance open-source Quantum Monte 
       Carlo (QMC) simulation code."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "http://www.qmcpack.org/"
    url      = "https://github.com/QMCPACK/qmcpack/archive/v3.1.0.tar.gz"

    version('3.1.0', 'bdf3acd090557acdb6cab5ddbf7c7960')
    version('3.0.0', '75f9cf70e6cc6d8b7ff11a86340da43d')

    #
    variant('cuda', default=False, description='Enable CUDA and GPU acceleration.')
    variant('complex', default=True, description='Build the complex (general twist/k-point) version')
    variant('debug', default=False, description='Build debug version')
   

    # if '+cuda' in spec:
    #    variant('mixed', default=True, description='Build the mixed precision (mixing double/float) version')
    # else:
    variant('mixed', default=False, description='Build the mixed precision (mixing double/float) version for cuda')

    depends_on('cmake@2.8.0:', type='build')
    depends_on('mpi')
    depends_on('libxml2')
    depends_on('hdf5+mpi')
    depends_on('boost')
    depends_on('blas')
    depends_on('lapack')
    depends_on('fftw')
    depends_on('cuda', when='+cuda')
    depends_on('cuda', when='+mixed')
   
    # qmca needs 
    # depends_on('python', type=('build', 'run'))
    # depends_on('py-numpy', type=('build', 'run'))
    # depends_on('py-matplotlib', type=('build', 'run'))

    depends_on('espresso@5.3.0+qmchdf+mpi+openmp~elpa~hdf5') 

    def cmake_args(self):
        args = []

        filter_file(r'$ENV{LIBXML2_HOME}/lib',
                    '${LIBXML2_HOME}/lib $ENV{LIBXML2_HOME}/lib',
                    'CMake/FindLibxml2QMC.cmake')
  
        print dir(self.spec['hdf5'].prefix)
        print self.spec['boost'].prefix

        if 'cxxflags' in self.compiler.flags:
            cxx_flags = ' '.join(self.compiler.flags['cxxflags'])
            args.append('-DCMAKE_CXX_FLAGS={0}'.format(cxx_flags))

        if 'cflags' in self.compiler.flags:
            c_flags = ' '.join(self.compiler.flags['cflags'])
            args.append('-DCMAKE_C_FLAGS={0}'.format(c_flags))

        args.append('-DCMAKE_C_COMPILER={0}'.format(self.spec['mpi'].mpicc ))
        args.append('-DCMAKE_CXX_COMPILER={0}'.format(self.spec['mpi'].mpicxx ))
        args.append('-DMPI_BASE_DIR:PATH={0}'.format(self.spec['mpi'].prefix ))
        args.append('-DLIBXML2_HOME={0}'.format(self.spec['libxml2'].prefix))
        args.append('-DLibxml2_INCLUDE_DIRS={0}'.format(self.spec['libxml2'].prefix.include))
        args.append('-DLibxml2_LIBRARY_DIRS={0}'.format(self.spec['libxml2'].prefix.lib))
        args.append('-DFFTW_HOME={0}'.format(self.spec['fftw'].prefix))
        args.append('-DBOOST_ROOT={0}'.format(self.spec['boost'].prefix))
        args.append('-DHDF5_ROOT={0}'.format(self.spec['hdf5'].prefix))
        args.append('-DFFTW_INCLUDE_DIRS={0}'.format(self.spec['fftw'].prefix.include))
        args.append('-DFFTW_LIBRARY_DIRS={0}'.format(self.spec['fftw'].prefix.lib))
        

        if '+cuda' in self.spec:
            args.append('-D QMC_CUDA=1')

        if '+mixed' in self.spec:
            args.append('-D QMC_CUDA=1')
            args.append('-D QMC_MIXED_PRECISION=1')

        return args

    def install(self, spec, prefix):
        """Make the install targets"""
        with working_dir(self.build_directory):
            # qmcpack doesn't have a make install
            # We have to do our own install here.
            mkdirp(prefix.include)
            install_tree(join_path(self.build_directory, 'include'),
                         prefix.include)
                         
            mkdirp(prefix.lib)
            install_tree(join_path(self.build_directory, 'lib'),
                         prefix.lib)
                         
            
            mkdirp(prefix.bin)
            install_tree(join_path(self.build_directory, 'bin'),
                         prefix.bin)


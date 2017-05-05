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
import glob,os,numbers

def isIntegral(x):
    """True for any integer value"""
    try:
        return isinstance(int(x), numbers.Integral) and not isinstance(x, bool)
    except ValueError:
        return False

class ChomboXsdk(Package):
    """Chombo is a Adaptive Mesh Refinement (AMR) C++ framework/library...
    """

    # Find out more about Chombo
    homepage = "http://chombo.lbl.gov/"
    url = "http://bitbucket.org/drhansj/chombo-xsdk/get/xsdk-0.2.0a.tar.bz2"

    # Versions available
    version('xsdk-0.2.0', git='http://bitbucket.org/drhansj/chombo-xsdk.git', commit='71d856c')
    version('develop'   , git='http://bitbucket.org/drhansj/chombo-xsdk.git', tag='master')

    # Build options/variants
    variant('dim'      , default=2    , description = 'Set the physical dimension',values=isIntegral)
    variant('debug'    , default=False, description = 'Build with debugging symbols')
    variant('opt'      , default=True , description = 'Build using compiler optimizations')
    variant('namespace', default=False, description = 'Put Chombo in a namespace')
    variant('mpi'      , default=True , description = 'Compile with MPI support')
    variant('use_eb'   , default=False, description = 'Compile with Embedded Boundary support')
    variant('use_hdf'  , default=True , description = 'Compile with HDF5 I/O support')
    variant('use_petsc', default=True , description = 'Compile with PETSc support')

    # Chombo dependencies for xSDK build
    depends_on('blas')
    depends_on('lapack')

    depends_on('mpi', when='+mpi')

    depends_on('hdf5~mpi~fortran', when='+use_hdf~mpi')
    depends_on('hdf5+mpi~fortran', when='+use_hdf+mpi')

    depends_on('petsc@xsdk-0.2.0~mpi~hypre~superlu-dist~hdf5+int64', when='@xsdk-0.2.0+use_petsc~mpi')
    depends_on('petsc@xsdk-0.2.0+mpi+int64'                        , when='@xsdk-0.2.0+use_petsc+mpi')

    depends_on('petsc@develop~mpi~hypre~superlu-dist~hdf5+int64', when='@develop+use_petsc~mpi')
    depends_on('petsc@develop+mpi+int64'                        , when='@develop+use_petsc+mpi')

    # Convert Python boolean False/True to strings "FALSE"/"TRUE"
    def boolToChombo(self, value):
        return str(value).upper()

    def install(self, spec, prefix):
        options = []

        # Set up all the options for the Chombo build
        options.append('DIM=%s'       %                   spec.variants['dim'].value)
        options.append('DEBUG=%s'     % self.boolToChombo(spec.variants['debug'].value))
        options.append('OPT=%s'       % self.boolToChombo(spec.variants['opt'].value))
        options.append('NAMESPACE=%s' % self.boolToChombo(spec.variants['namespace'].value))
        options.append('MPI=%s'       % self.boolToChombo(spec.variants['mpi'].value))
        options.append('USE_EB=%s'    % self.boolToChombo(spec.variants['use_eb'].value))
        options.append('USE_HDF=%s'   % self.boolToChombo(spec.variants['use_hdf'].value))
        options.append('USE_PETSC=%s' % self.boolToChombo(spec.variants['use_petsc'].value))

        if spec.variants['mpi']:
          options.append('RUN=%s -np 2 ./' % join_path(spec['mpi'].prefix.bin,'mpirun'))
        else:
          options.append('RUN=./')

        if '+use_hdf' in spec:
          options.append('HDFINCFLAGS=-I%s/include' % spec['hdf5'].prefix)
          options.append('HDFLIBFLAGS=-L%s/lib -lhdf5 -lz' % spec['hdf5'].prefix)
          options.append('HDFMPIINCFLAGS=-I%s/include' % spec['hdf5'].prefix)
          options.append('HDFMPILIBFLAGS=-L%s/lib -lhdf5 -lz' % spec['hdf5'].prefix)

        options.append('syslibflags=%s %s' % (spec['lapack'].libs,spec['blas'].libs))

        # Build library
        make('--directory=lib','lib',*options)

        # Build unit tests
        make('--directory=lib','all',*options)

        # Run unit tests
        make('--directory=lib','run',*options)

        # TODO - Build and run example

        # Need to install by hand

        # Get and create the target 'include' and 'lib'
        headers_location = self.prefix.include
        mkdirp(headers_location)

        libs_location = self.prefix.lib
        mkdirp(libs_location)

        # Install the include files
        headers = glob.glob(join_path(self.stage.source_path, 'lib', 'include', '*.H'))
        for h in headers:
          install(h, headers_location)

        # Install the library
        libs = glob.glob(join_path(self.stage.source_path, 'lib', '*.a'))
        for l in libs:
          install(l, libs_location)

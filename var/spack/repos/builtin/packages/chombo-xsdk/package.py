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
import numbers
import shutil


def isIntegral(x):
    """True for any integer value"""
    try:
        return isinstance(int(x), numbers.Integral) and not isinstance(x, bool)
    except ValueError:
        return False


class ChomboXsdk(Package):
    """Chombo is an Adaptive Mesh Refinement (AMR) C++ framework/library...
    """

    # Find out more about Chombo
    homepage = "http://chombo.lbl.gov/"
    url = "http://bitbucket.org/drhansj/chombo-xsdk/get/xsdk-0.2.0a.tar.bz2"

    # Versions available
    version('xsdk-0.2.0', git='http://bitbucket.org/drhansj/chombo-xsdk.git', tag='xsdk-0.2.0')
    version('develop', git='http://bitbucket.org/drhansj/chombo-xsdk.git', tag='master')

    # Build options/variants
    variant('dim', default=2, description='Set the physical dimension', values=isIntegral)
    variant('debug', default=False, description='Build with debugging symbols')
    variant('opt', default=True, description='Build using compiler optimizations')
    variant('namespace', default=False, description='Put Chombo in a namespace')
    variant('mpi', default=True, description='Compile with MPI support')
    variant('use_eb', default=False, description='Compile with Embedded Boundary support')
    variant('use_hdf', default=True, description='Compile with HDF5 I/O support')
    variant('use_petsc', default=True, description='Compile with PETSc support')

    # Chombo dependencies for xSDK build
    depends_on('blas')
    depends_on('lapack')

    depends_on('mpi', when='+mpi')

    depends_on('hdf5~mpi', when='+use_hdf~mpi')
    depends_on('hdf5+mpi', when='+use_hdf+mpi')

    depends_on('petsc@xsdk-0.2.0~mpi~hypre~superlu-dist~hdf5', when='@xsdk-0.2.0+use_petsc~mpi')
    depends_on('petsc@xsdk-0.2.0+mpi', when='@xsdk-0.2.0+use_petsc+mpi')

    depends_on('petsc@develop~mpi~hypre~superlu-dist~hdf5', when='@develop+use_petsc~mpi')
    depends_on('petsc@develop+mpi', when='@develop+use_petsc+mpi')

    # Convert Python boolean False/True to strings "FALSE"/"TRUE"
    def boolToChombo(self, value):
        return str(value).upper()

    def install(self, spec, prefix):
        options = []

        # Set up all the options for the Chombo build
        options.append('DIM=%s' % spec.variants['dim'].value)
        options.append('DEBUG=%s' %
                       self.boolToChombo(spec.variants['debug'].value))
        options.append('OPT=%s' %
                       self.boolToChombo(spec.variants['opt'].value))
        options.append('NAMESPACE=%s' %
                       self.boolToChombo(spec.variants['namespace'].value))
        options.append('MPI=%s' %
                       self.boolToChombo(spec.variants['mpi'].value))
        options.append('USE_EB=%s' %
                       self.boolToChombo(spec.variants['use_eb'].value))
        options.append('USE_HDF=%s' %
                       self.boolToChombo(spec.variants['use_hdf'].value))
        options.append('USE_PETSC=%s' %
                       self.boolToChombo(spec.variants['use_petsc'].value))

        if spec.variants['mpi']:
            options.append('RUN=%s -np 2 ./' %
                           join_path(spec['mpi'].prefix.bin, 'mpirun'))
        else:
            options.append('RUN=./')

        if spec.variants['use_hdf']:
            options.append('HDFINCFLAGS=-I%s/include' % spec['hdf5'].prefix)
            options.append('HDFLIBFLAGS=-L%s/lib -lhdf5 -lz' %
                           spec['hdf5'].prefix)
            options.append('HDFMPIINCFLAGS=-I%s/include' % spec['hdf5'].prefix)
            options.append('HDFMPILIBFLAGS=-L%s/lib -lhdf5 -lz' %
                           spec['hdf5'].prefix)

        options.append('syslibflags=%s %s' %
                       (spec['lapack'].libs, spec['blas'].libs))

        # Where all the include files will go
        headers_dest = self.prefix.include
        mkdirp(headers_dest)

        # Install the library source directory
        lib_src  = join_path(self.stage.source_path, 'lib')
        lib_dest = self.prefix.lib
        shutil.copytree(lib_src, lib_dest)

        # Modify the "Make.defs.local" file in installation under "lib/mk"
        make_defs_local_filename = join_path(
            self.prefix.lib, 'mk', 'Make.defs.local')
        make_defs_local = open(make_defs_local_filename, 'w')

        make_defs_local.write('makefiles+=Make.defs.local\n')
        make_defs_local.write('\n')

        make_defs_local.write('#begin  -- dont change this line\n')
        make_defs_local.write('\n')

        make_defs_local.write('CC=%s\n' % self.compiler.cc)
        make_defs_local.write('CXX=%s\n' % self.compiler.cxx)
        make_defs_local.write('FC=%s\n' % self.compiler.fc)

        if spec.variants['mpi']:
            make_defs_local.write('MPICXX=%s\n' % os.environ['MPICXX'])

        if spec.variants['use_petsc']:
            make_defs_local.write('PETSC_DIR=%s\n' % os.environ['PETSC_DIR'])

        make_defs_local.write('\n')

        for option in options:
            make_defs_local.write('%s\n' % option)
        make_defs_local.write('\n')

        make_defs_local.write('#end  -- dont change this line\n')

        make_defs_local.close()

        # Install the examples source directory
        example_src = join_path(self.stage.source_path, 'releasedExamples')
        example_dest = join_path(self.prefix, "examples")
        shutil.copytree(example_src, example_dest)

        # Build library
        make('--directory=lib', 'lib', *options)

        # Build unit tests
        make('--directory=lib', 'all', *options)

        # Run unit tests
        make('--directory=lib', 'run', *options)

        # Install the include files
        header_files = glob.glob(
            join_path(self.stage.source_path, 'lib', 'include', '*.H'))
        for h in header_files:
            install(h, headers_dest)

        # Install the built libraries
        lib_files = glob.glob(join_path(self.stage.source_path, 'lib', '*.a'))
        for l in lib_files:
            install(l, lib_dest)

        # Build the examples (in situ)
        make('--directory=%s' % example_dest, 'example-only', *options)

        # Run the examples
        make('--directory=%s' % example_dest, 'run', *options)

        # Cleanup the examples
        make('--directory=%s' % example_dest, 'realclean', *options)

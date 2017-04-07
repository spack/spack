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


class Npb(MakefilePackage):
    """The NAS Parallel Benchmarks (NPB) are a small set of programs
    designed to help evaluate the performance of parallel supercomputers.
    The benchmarks are derived from computational fluid dynamics (CFD)
    applications and consist of five kernels and three pseudo-applications
    in the original "pencil-and-paper" specification (NPB 1). The benchmark
    suite has been extended to include new benchmarks for unstructured
    adaptive mesh, parallel I/O, multi-zone applications, and computational
    grids. Problem sizes in NPB are predefined and indicated as different
    classes. Reference implementations of NPB are available in commonly-used
    programming models like MPI and OpenMP (NPB 2 and NPB 3)."""

    homepage = "https://www.nas.nasa.gov/publications/npb.html"
    url      = "https://www.nas.nasa.gov/assets/npb/NPB3.3.1.tar.gz"

    version('3.3.1', '8e5ec2c819480759725df67833619911')

    # Valid Benchmark Names
    valid_names = (
        'is',  # Integer Sort, random memory access
        'ep',  # Embarrassingly Parallel
        'cg',  # Conjugate Gradient, irregular memory access and communication
        'mg',  # Multi-Grid on a sequence of meshes, long- and short-distance
               # communication, memory intensive
        'ft',  # discrete 3D fast Fourier Transform, all-to-all communication
        'bt',  # Block Tri-diagonal solver
        'sp',  # Scalar Penta-diagonal solver
        'lu',  # Lower-Upper Gauss-Seidel solver
    )

    # Valid Benchmark Classes
    valid_classes = (
        'S',            # Small for quick test purposes
        'W',            # Workstation size
        'A', 'B', 'C',  # standard test problems
                        # ~4X size increase going from one class to the next
        'D', 'E',       # large test problems
                        # ~16X size increase from each of the previous classes
    )

    # TODO: Combine these into a single mutually exclusive variant
    variant('mpi',    default=True,  description='Build the MPI implementation')
    variant('openmp', default=False, description='Build the OpenMP implementation')
    variant('serial', default=False, description='Build the serial version')

    # TODO: Convert these to non-exclusive multi-valued variants
    variant('names', default=','.join(valid_names),
            description='Benchmark names (comma separated list)')
    variant('classes', default=','.join(valid_classes),
            description='Benchmark classes (comma separated list)')
    # This variant only applies to the MPI implementation
    variant('nprocs', default='1,2,4,8,16,32,64,128',
            description='Number of processes (comma separated list)')

    depends_on('mpi@2:', when='+mpi')

    phases = ['edit', 'install']

    # Cannot be built in parallel
    parallel = False

    @property
    def build_directory(self):
        if '+mpi' in self.spec:
            implementation = 'MPI'
        elif '+openmp' in self.spec:
            implementation = 'OMP'
        elif '+serial' in self.spec:
            implementation = 'SER'
        else:
            raise RuntimeError('You must choose an implementation to build')

        return 'NPB{0}-{1}'.format(self.version.up_to(2), implementation)

    def edit(self, spec, prefix):
        names   = spec.variants['names'].value.split(',')
        classes = spec.variants['classes'].value.split(',')
        nprocs  = spec.variants['nprocs'].value.split(',')

        if '+mpi' in spec:
            definitions = {
                # Parallel Fortran
                'MPIF77':     spec['mpi'].mpif77,
                'FLINK':      spec['mpi'].mpif77,
                'FMPI_LIB':   spec['mpi'].libs.ld_flags,
                'FMPI_INC':   '-I' + spec['mpi'].prefix.include,
                'FFLAGS':     '-O3',
                'FLINKFLAGS': '-O3',
                # Parallel C
                'MPICC':      spec['mpi'].mpicc,
                'CLINK':      spec['mpi'].mpicc,
                'CMPI_LIB':   spec['mpi'].libs.ld_flags,
                'CMPI_INC':   '-I' + spec['mpi'].prefix.include,
                'CFLAGS':     '-O3',
                'CLINKFLAGS': '-O3',
                # Utilities C
                'CC':         spack_cc + ' -g',
                'BINDIR':     prefix.bin,
                'RAND':       'randi8',
            }
        elif '+openmp' in spec:
            definitions = {
                # Parallel Fortran
                'F77':        spack_f77,
                'FLINK':      spack_f77,
                'F_LIB':      '',
                'F_INC':      '',
                'FFLAGS':     '-O3 ' + self.compiler.openmp_flag,
                'FLINKFLAGS': '-O3 ' + self.compiler.openmp_flag,
                # Parallel C
                'CC':         spack_cc,
                'CLINK':      spack_cc,
                'C_LIB':      '-lm',
                'C_INC':      '',
                'CFLAGS':     '-O3 ' + self.compiler.openmp_flag,
                'CLINKFLAGS': '-O3 ' + self.compiler.openmp_flag,
                # Utilities C
                'UCC':        spack_cc,
                'BINDIR':     prefix.bin,
                'RAND':       'randi8',
                'WTIME':      'wtime.c',
            }
        elif '+serial' in spec:
            definitions = {
                # Parallel Fortran
                'F77':        spack_f77,
                'FLINK':      spack_f77,
                'F_LIB':      '',
                'F_INC':      '',
                'FFLAGS':     '-O3',
                'FLINKFLAGS': '-O3',
                # Parallel C
                'CC':         spack_cc,
                'CLINK':      spack_cc,
                'C_LIB':      '-lm',
                'C_INC':      '',
                'CFLAGS':     '-O3',
                'CLINKFLAGS': '-O3',
                # Utilities C
                'UCC':        spack_cc,
                'BINDIR':     prefix.bin,
                'RAND':       'randi8',
                'WTIME':      'wtime.c',
            }

        with working_dir(self.build_directory):
            with open('config/make.def', 'w') as make_def:
                for key in definitions:
                    make_def.write('{0} = {1}\n'.format(
                        key, definitions[key]))

            with open('config/suite.def', 'w') as suite_def:
                for name in names:
                    for classname in classes:
                        # Classes C, D and E are not available for DT
                        if name == 'dt' and classname in ('C', 'D', 'E'):
                            continue

                        # Class E is not available for IS
                        if name == 'is' and classname == 'E':
                            continue

                        if '+mpi' in spec:
                            for nproc in nprocs:
                                suite_def.write('{0}\t{1}\t{2}\n'.format(
                                    name, classname, nproc))
                        else:
                            suite_def.write('{0}\t{1}\n'.format(
                                name, classname))

    def install(self, spec, prefix):
        mkdir(prefix.bin)

        with working_dir(self.build_directory):
            make('suite')

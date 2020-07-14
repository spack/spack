# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class CcsQcd(MakefilePackage):
    """This program benchmarks the performance of a linear equation solver
       with a large sparse coefficient matrix appering in a lattice QCD
       probrem. Lattice QCD describes the property of protons, neutrons and
       neucleons in terms of more fundamental interacting elementary particles
       gluon and quarks."""

    homepage = "https://github.com/fiber-miniapp/ccs-qcd"
    git      = "https://github.com/fiber-miniapp/ccs-qcd.git"

    version('master', branch='master')
    version('1.2.1', commit='d7c6b6923f35a824e997ba8db5bd12dc20dda45c')

    variant('class', default=1, values=('1', '2', '3', '4', '5', '6'),
            description='This miniapp has five problem classes, for which the'
            ' first three are relatively small problems just for testing'
            ' this miniapp itself. The remaining two are the target problem'
            ' sizes for the HPCI FS evaluation.',
            multi=False)

    depends_on('mpi')

    parallel = False

    def edit(self, spec, prefix):
        if spec.satisfies('%gcc') and spec.satisfies('arch=aarch64:'):
            chgopt = 'FFLAGS  =-O3 -ffixed-line-length-132 -g -fopenmp' \
                     ' -mcmodel=large -funderscoring'
            filter_file('FFLAGS  =.*', chgopt, join_path(
                self.stage.source_path, 'src', 'make.gfortran.inc'))
        if '%fj' in spec:
            filter_file('mpifrtpx', spec['mpi'].mpifc, join_path(
                        self.stage.source_path, 'src', 'make.fx10.inc'))
            filter_file('mpifccpx', spec['mpi'].mpicc, join_path(
                        self.stage.source_path, 'src', 'make.fx10.inc'))
        else:
            filter_file('mpif90', spec['mpi'].mpifc, join_path(
                        self.stage.source_path, 'src', 'make.gfortran.inc'))
            filter_file('mpicc', spec['mpi'].mpicc, join_path(
                        self.stage.source_path, 'src', 'make.gfortran.inc'))

    def build(self, spec, prefix):
        ccs_class = 'CLASS=' + spec.variants['class'].value
        with working_dir('src'):
            if '%fj' in spec:
                make('MAKE_INC=make.fx10.inc', ccs_class)
            else:
                make('MAKE_INC=make.gfortran.inc', ccs_class)

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install('./src/ccs_qcd_solver_bench_class' +
                spec.variants['class'].value, prefix.bin)

# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
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

    variant(
        'class',
        default='1',
        values=(
            '1',  # 8x8x8x32 (default MPI config: 1x1x1)
            '2',  # 32x32x32x32 (default MPI config: 4x4x4)
            '3',  # 64x64x64x32 (default MPI config: 8x8x8)
            '4',  # 160x160x160x160 (default MPI config: 20x20x20)
            '5',  # 256x256x256x256 (default MPI config: 32x32x32)
            '6'   # 192x192x192x192 (default MPI config: 24x24x24)
        ),
        description='This miniapp has five problem classes, for which the' +
            ' first three are relatively small problems just for testing' +
            ' this miniapp itself. The remaining two are the target problem' +
            ' sizes for the HPCI FS evaluation.',
        multi=False
    )

    depends_on('mpi')

    def edit(self, spec, prefix):
        if '%fj' in spec:
            filter_file('mpifrtpx', spec['mpi'].mpifc, './src/make.fx10.inc')
            filter_file('mpifccpx', spec['mpi'].mpicc, './src/make.fx10.inc')

    def build(self, spec, prefix):
        with working_dir('src'):
            if 'class=1' in spec:
                ccs_class = 'CLASS=1'
            elif 'class=2' in spec:
                ccs_class = 'CLASS=2'
            elif 'class=3' in spec:
                ccs_class = 'CLASS=3'
            elif 'class=4' in spec:
                ccs_class = 'CLASS=4'
            elif 'class=5' in spec:
                ccs_class = 'CLASS=5'
            elif 'class=6' in spec:
                ccs_class = 'CLASS=6'

            make('CONFIG_GEN', '%s' % ccs_class)

            if '%fj' in spec:
                make('MAKE_INC=make.fx10.inc', '%s' % ccs_class)
            else:
                make('MAKE_INC=make.gfortran.inc', '%s' % ccs_class)

            self.ccs_class = ccs_class

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install('./src/ccs_qcd_solver_bench_class%s' % self.ccs_class[-1:],
                prefix.bin)

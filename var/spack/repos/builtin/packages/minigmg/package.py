# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class Minigmg(Package):
    """miniGMG is a compact benchmark for understanding the performance
    challenges associated with geometric multigrid solvers
    found in applications built from AMR MG frameworks
    like CHOMBO or BoxLib when running
    on modern multi- and manycore-based supercomputers.
    It includes both productive reference examples as well as
    highly-optimized implementations for CPUs and GPUs.
    It is sufficiently general that it has been used to evaluate
    a broad range of research topics including PGAS programming models
    and algorithmic tradeoffs inherit in multigrid. miniGMG was developed
    under the CACHE Joint Math-CS Institute.

    Note, miniGMG code has been supersceded by HPGMG. """

    homepage = "http://crd.lbl.gov/departments/computer-science/PAR/research/previous-projects/miniGMG/"
    url      = "http://crd.lbl.gov/assets/Uploads/FTG/Projects/miniGMG/miniGMG.tar.gz"

    version('master', sha256='1c2d27496a881f655f5e849d6a7a132625e535739f82575991c511cc2cf899ac')

    version('local', branch='minigmg', git='https://github.com/FindHao/minigmg')

    variant('debug', default=False, description='Enable debug flag')
    variant('simde', default=False, description='enable simde')
    variant('opt', default=False,
            description='enable -Ofast -D__PREFETCH_NEXT_PLANE_FROM_DRAM -D__FUSION_RESIDUAL_RESTRICTION')

    depends_on('mpi')
    depends_on('simde', when="+simde")

    phases = ['build', 'install']

    def build(self, spec, prefix):
        cc = Executable(spec['mpi'].mpicc)
        if spec.satisfies('target=aarch64:'):
            arm_archflag = '-Daarch64'
        else:
            arm_archflag = ''
        if spec.satisfies('+debug'):
            self.debug_flags = '-g'
        else:
            self.debug_flags = ''

        if spec.satisfies('+simde'):
            operators_source_file = 'operators.avx.c'
        else:
            operators_source_file = 'operators.ompif.c'

        if spec.satisfies('+opt'):
            opt_flag = '-D__PREFETCH_NEXT_PLANE_FROM_DRAM -D__FUSION_RESIDUAL_RESTRICTION'
            fast_flag = '-Ofast'
            COLLABORATIVE_THREADING_flag = ''
        else:
            opt_flag = ''
            fast_flag = ''
            COLLABORATIVE_THREADING_flag = '-D__COLLABORATIVE_THREADING=6'

        cc('-O3', fast_flag, self.compiler.openmp_flag, self.debug_flags, 'miniGMG.c',
            'mg.c', 'box.c', 'solver.c', operators_source_file, 'timer.x86.c',
            '-D__MPI', COLLABORATIVE_THREADING_flag, opt_flag,
            '-D__TEST_MG_CONVERGENCE', '-D__PRINT_NORM', '-D__USE_BICGSTAB', arm_archflag,
            '-o', 'run.miniGMG', '-lm')

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        install('run.miniGMG', prefix.bin)
        mkdir(prefix.jobs)
        install('job*', prefix.jobs)

# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Alpaka(CMakePackage):
    """Abstraction Library for Parallel Kernel Acceleration."""

    homepage = "https://alpaka.readthedocs.io"
    url      = "https://github.com/alpaka-group/alpaka/archive/refs/tags/0.6.0.tar.gz"
    git      = "https://github.com/alpaka-group/alpaka.git"

    maintainers = ['vvolkl']

    version('develop', branch='develop')
    version('0.6.0', sha256='7424ecaee3af15e587b327e983998410fa379c61d987bfe923c7e95d65db11a3')

    variant("acc_cpu_b_seq_t_seq", default=True, description="Enable the serial CPU back-end")
    variant("acc_cpu_b_seq_t_threads", default=True,
            description="Enable the threads CPU block thread back-end")
    variant("acc_cpu_b_seq_t_fibers", default=False, description="Enable the fibers CPU block thread back-end")
    variant("acc_cpu_b_tbb_t_seq", default=False, description="Enable the TBB CPU grid block back-end")
    variant("acc_cpu_b_omp2_t_seq", default=False, description="Enable the OpenMP 2.0 CPU grid block back-end")
    variant("acc_cpu_b_seq_t_omp2", default=False, description="Enable the OpenMP 2.0 CPU block thread back-end")
    variant("acc_any_bt_omp5", default=False, description="Enable the OpenMP 5.0 CPU block and block thread back-end")
    variant("acc_any_bt_oacc", default=False, description="Enable the OpenACC block and block thread back-end")
    variant("examples", default=False, description="Build alpaka examples")

    depends_on('boost')

    def cmake_args(self):
        args = [self.define_from_variant("ALPAKA_ACC_CPU_B_SEQ_T_SEQ_ENABLE",
                                         "acc_cpu_b_seq_t_seq"),
                self.define_from_variant("ALPAKA_ACC_CPU_B_SEQ_T_THREADS_ENABLE",
                                         "acc_cpu_b_seq_t_threads"),
                self.define_from_variant("ALPAKA_ACC_CPU_B_SEQ_T_FIBERS_ENABLE",
                                         "acc_cpu_b_seq_t_fibers"),
                self.define_from_variant("ALPAKA_ACC_CPU_B_TBB_T_SEQ_ENABLE",
                                         "acc_cpu_b_tbb_t_seq"),
                self.define_from_variant("ALPAKA_ACC_CPU_B_OMP2_T_SEQ_ENABLE",
                                         "acc_cpu_b_omp2_t_seq"),
                self.define_from_variant("ALPAKA_ACC_CPU_B_SEQ_T_OMP2_ENABLE",
                                         "acc_cpu_b_seq_t_omp2"),
                self.define_from_variant("ALPAKA_ACC_ANY_BT_OMP5_ENABLE",
                                         "acc_any_bt_omp5"),
                self.define_from_variant("ALPAKA_ACC_ANY_BT_OACC_ENABLE",
                                         "acc_any_bt_oacc"),
                self.define_from_variant("alpaka_BUILD_EXAMPLES",
                                         "examples"),
                # need to define, as it is explicitly declared as an option by alpaka:
                self.define("BUILD_TESTING", self.run_tests),
                ]
        return args

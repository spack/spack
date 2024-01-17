# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Countdown(CMakePackage, CudaPackage):
    """COUNTDOWN is a tool for identifying and automatically reducing the power
    consumption of the computing elements, during communication and
    synchronization primitives, filtering out phases which would detriment the
    time to solution of the application."""

    homepage = "https://github.com/EEESlab/countdown"
    url = "https://github.com/EEESlab/countdown/archive/refs/tags/v1.1.0.tar.gz"

    license("BSD-3-Clause")

    maintainers = ['f-tesser', 'danielecesarini']

    version("1.1.0", sha256="0fd2703bc8fcf69cbdb6122e4974a79b3987e897e9d4c86f5d3a1631731522bd")

    variant("cuda", default=False, description="Build with CUDA")
    variant("shared", default=True, description="Build shared libraries")
    variant("no_profiling", default=False, description="Disable MPI profiling")
    variant("no_acc_mpi", default=False, description="Disable the instrumentation of all accessory MPI functions")
    variant("no_p2p_mpi", default=False, description="Disable the instrumentation of all point-to-point MPI functions")
    variant("debug_mpi", default=False, description="Enable the debug prints on MPI functions")
    variant("mosquitto", default=False, description="Enable MQTT message passing")
    variant("hwp_auto_discovery", default=True, description="Autodiscovery of hwp-states")
    variant("hwp_manual_set", default=False, description="Manual set if hwp-states are available")
    variant("cpufreq_manual_set", default=True, description="Manual set of cpufreq interface")

    depends_on('cmake@3.0.0:', type='build')
    depends_on('hwloc', type='link')
    depends_on('mpi@3.0.0:', type='link')
    depends_on("cuda", when="+cuda")
    depends_on("mosquitto", when="+mosquitto", type='link')

    def cmake_args(self):
        args = [
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
            self.define_from_variant("CNTD_ENABLE_CUDA", "cuda"),
            self.define_from_variant("CNTD_DISABLE_PROFILING_MPI", "no_profiling"),
            self.define_from_variant("CNTD_DISABLE_ACCESSORY_MPI", "no_acc_mpi"),
            self.define_from_variant("CNTD_DISABLE_P2P_MPI", "no_p2p_mpi"),
            self.define_from_variant("CNTD_ENABLE_DEBUG_MPI", "debug_mpi"),
            self.define_from_variant("CNTD_ENABLE_MOSQUITTO", "mosquitto"),
            self.define_from_variant("CNTD_HWP_AUTO_DISCOVER", "hwp_auto_discovery"),
            self.define_from_variant("CNTD_HWP_DISCOVERED", "hwp_manual_set"),
            self.define_from_variant("CNTD_USE_CPUFREQ", "cpufreq_manual_set"),
        ]

        return args

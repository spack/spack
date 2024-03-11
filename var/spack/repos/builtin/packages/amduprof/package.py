# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Amduprof(Package):
    """AMD uProf ("MICRO-prof") is a software profiling analysis tool for
    x86 applications running on Windows, Linux and FreeBSD operating systems
    and provides event information unique to the AMD "Zen"-based processors
    and AMD Instinct(tm) MI Series accelerators.
    """

    homepage = "https://developer.amd.com/amd-uprof/"
    url = "https://download.amd.com/developer/eula/uprof/AMDuProf_Linux_x64_4.2.850.tar.bz2"

    maintainers("zzzoom")

    version("4.2.850", sha256="f2d7c4eb9ec9c32845ff8f19874c1e6bcb0fa8ab2c12e73addcbf23a6d1bd623")

    # TODO: build Power Profiling driver on Linux
    # TODO: ROCm for GPU tracing and profiling
    # TODO: BCC and eBPF for OS tracing

    conflicts("platform=darwin")

    def install(self, spec, prefix):
        install_tree(".", prefix)

# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Amduprof(Package):
    """AMD uProf is a software profiling analysis tool for x86 applications
    and provides event information unique to the AMD "Zen"-based processors."""

    homepage = "https://developer.amd.com/amd-uprof/"
    url = "https://developer.amd.com/wordpress/media/files/AMDuProf_Linux_x64_3.5.671.tar.bz2"

    version("3.5.671", sha256="a73066305228658a14af5ecd6cf45a1aa47ae94f7e9d14db31f43013d3ef1a43")

    depends_on("binutils", type="run")

    # TODO: build Power Profiling driver on Linux
    # TODO: ROCm for GPU tracing and profiling
    # TODO: BCC and eBPF for OS tracing

    conflicts("platform=darwin")

    def install(self, spec, prefix):
        install_tree(".", prefix)

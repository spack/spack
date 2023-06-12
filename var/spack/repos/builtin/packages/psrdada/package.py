# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Psrdada(AutotoolsPackage, CudaPackage):
    """Open source software to process some types of astronomy data."""

    homepage = "https://psrdada.sourceforge.net/"
    git = "https://git.code.sf.net/p/psrdada/code"

    version("master", branch="master")

    conflicts("~cuda", msg="You must specify +cuda")
    conflicts("cuda_arch=none", when="+cuda", msg="You must specify the CUDA architecture")

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("python")
    depends_on("cuda@:11.7", type="build")

    def install(self, spec, prefix):
        make()
        make("install")

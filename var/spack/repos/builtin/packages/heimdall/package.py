# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Heimdall(AutotoolsPackage, CudaPackage):
    """GPU accelerated transient detection pipeline"""

    homepage = "https://sourceforge.net/projects/heimdall-astro/"
    git = "https://git.code.sf.net/p/heimdall-astro/code"

    version("1.0", branch="master")

    conflicts("~cuda", msg="You must specify +cuda")
    conflicts("cuda_arch=none", when="+cuda", msg="You must specify the CUDA architecture")

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("cuda@:11.7")

    # Pass the cuda architecture to DEDISP and PSRDADA for building
    for arch in CudaPackage.cuda_arch_values:
        depends_on("dedisp +cuda cuda_arch=%s" % arch,
                   when="+cuda cuda_arch=%s" % arch)

        depends_on("psrdada +cuda cuda_arch=%s" % arch,
                   when="+cuda cuda_arch=%s" % arch)

    def setup_run_environment(self, env):
        env.prepend_path("PATH", self.spec["psrdada"].prefix.bin)
        env.prepend_path("LD_LIBRARY_PATH", self.spec["dedisp"].prefix.lib)
        env.prepend_path("LD_LIBRARY_PATH", self.spec["cuda"].prefix.lib)

    def configure_args(self):
        # Heimdall requires some special flags for configure
        args = ["--with-psrdada-dir=" + self.spec["psrdada"].prefix,
                "--with-dedisp-dir=" + self.spec["dedisp"].prefix,
                "--with-cuda-dir=" + self.spec["cuda"].prefix]
        return args

    def install(self, spec, prefix):
        make()
        make("install")

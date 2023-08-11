# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Fftx(CMakePackage, CudaPackage, ROCmPackage):
    """FFTX is the exascale follow-on to the FFTW open source discrete FFT
    package for executing the Fast Fourier Transform as well as higher-level
    operations composed of linear operations combined with DFT transforms."""

    homepage = "https://spiral.net"
    url = "https://github.com/spiral-software/fftx/archive/refs/tags/1.0.3.tar.gz"
    git = "https://github.com/spiral-software/fftx.git"

    maintainers("spiralgen")

    version("develop", branch="develop")
    version("main", branch="main")
    version("1.1.1", sha256="5cbca66ef09eca02ee8f336f58eb45cfac69cfb29cd6eb945852ad74085d8a60")
    version("1.1.0", sha256="a6f95605abc11460bbf51839727a456a31488e27e12a970fc29a1b8c42f4e3b5")

    depends_on("spiral-software")
    depends_on("spiral-package-fftx")
    depends_on("spiral-package-simt")
    depends_on('spiral-package-mpi')
    depends_on('spiral-package-jit')

    conflicts("+rocm", when="+cuda", msg="FFTX only supports one GPU backend at a time")

    @run_before("cmake")
    def create_lib_source_code(self):
        #  What config should be built -- driven by spec
        spec = self.spec
        backend = "CPU"
        if "+cuda" in spec:
            backend = "CUDA"
        if "+rocm" in spec:
            backend = "HIP"
        self.build_config = "-D_codegen=%s" % backend

        #  From the root directory run the config-fftx-libs.sh script
        ##  with working_dir(join_path(self.stage.source_path, "src", "library")):
        with working_dir(self.stage.source_path):
            bash = which("bash")
            bash("./config-fftx-libs.sh", backend)

    def cmake_args(self):
        spec = self.spec
        args = ["-DSPIRAL_HOME:STRING={0}".format(spec["spiral-software"].prefix)]
        args.append("-DCMAKE_INSTALL_PREFIX:PATH={0}".format(self.stage.source_path))
        args.append(self.build_config)
        print("Args = " + str(args))
        return args

    @property
    def build_targets(self):
        ##  return ["-j1", "install"]
        return ["install"]

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        mkdirp(prefix.CMakeIncludes)
        ##  mkdirp(prefix.examples)
        mkdirp(prefix.include)
        mkdirp(prefix.lib)

        with working_dir(self.stage.source_path):
            files = ("License.txt", "README.md", "ReleaseNotes.md")
            for fil in files:
                install(fil, prefix)

        with working_dir(self.stage.source_path):
            install_tree("bin", prefix.bin)
            install_tree("CMakeIncludes", prefix.CMakeIncludes)
            ##  install_tree("examples", prefix.examples)
            install_tree("include", prefix.include)
            install_tree("lib", prefix.lib)

    def setup_dependent_build_environment(self, env, dependent_spec):
        env.set("FFTX_HOME", self.prefix)

    def setup_dependent_run_environment(self, env, dependent_spec):
        env.set("FFTX_HOME", self.prefix)

    def setup_run_environment(self, env):
        env.set("FFTX_HOME", self.prefix)

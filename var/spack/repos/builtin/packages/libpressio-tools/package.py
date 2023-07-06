# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class LibpressioTools(CMakePackage):
    """General Utilities for LibPressio"""

    homepage = "https://github.com/robertu94/pressio-tools"
    url = "https://github.com/robertu94/pressio-tools/archive/refs/tags/0.0.15.tar.gz"
    git = "https://github.com/robertu94/pressio-tools"

    maintainers("robertu94")
    tags = ["e4s"]

    version("master", branch="master")
    version("0.3.0", sha256="2f309557df3e8df9e492691213933865a5dbfb051c03404e33918f4765223025")
    version("0.2.0", sha256="75048950f0dfa0e20f2651991875822f36fceb84bdda12d1c0361d49912392b8")
    version("0.1.6", sha256="a67a364f46dea29ff1b3e5c52c0a5abf2d9d53412fb8d424f6bd71252bfa7792")
    version("0.1.5", sha256="b35f495fae53df87dd2abf58c0c51ed17710b16aaa2d0842a543fddd3b2a8035")
    version("0.1.4", sha256="39adc4b09a63548a416ee4b1dcc87ec8578b15a176a11a2845c276c6c211f2d0")
    version("0.1.3", sha256="4e6c39061d6d829936dfeb569ea997854694ef1a46f112e306672ee1cc1567a0")
    version("0.1.2", sha256="a3379fd7c53c2eb0b5cdbf0e7eed37ae2a415f737885310d3da4d34fa55c618e")
    version("0.1.1", sha256="adec3ea9a12677c647fbc3a1f9909fde6f2dd5ed662ed0ee5cd753b26397643e")
    version("0.1.0", sha256="e016b1785f2dc5c8a8565ff3d7b50980788e057e61905a91ef1d16da73297a06")
    version("0.0.24", sha256="b369efcc17f339fdd5741d817f1b7908bd2b5df5686c5406c6b1123b0daa82c5")
    version("0.0.23", sha256="08a141be14e63e491216a89d45737040fc3450c5b793e6a4819cd06f876b2b0b")
    version("0.0.22", sha256="9fcb20a3bf24e139386e94b413f10087d65ed32d2eb93cc7be8e87d736da9766")
    version("0.0.21", sha256="2ffe1018ff86eca0928ab8bbf568b2cf7ab739f0e191e2722a6f5071dac4a153")
    version("0.0.20", sha256="cad3a1dff25ae1dc442821e72fe8f7495e098bd0ea52c3beeac1ceb721c60351")
    version("0.0.19", sha256="cc8a4bb5259b7b8e14248a1a741067a865a0db36645c878d346da983e74c9521")
    version("0.0.18", sha256="766fcf6c4bd475de66107d379c76805d6368d71ee83cade645f2b7cd27801718")
    version("0.0.17", sha256="cf76e8a929aa128d09f8f953171d5cf395223245bc81d2ea4e22099849e40b94")
    version("0.0.16", sha256="1299e441fb15666d1c8abfd40f3f52b1bf55b6bfda4bfcc71177eec37160a95e")
    version("0.0.15", sha256="bcdf865d77969a34e2d747034ceeccf5cb766a4c11bcc856630d837f442ee33e")

    depends_on("mpi", when="+mpi")
    depends_on("libpressio+libdistributed+mpi", when="+mpi")
    depends_on("libpressio", when="~mpi")
    depends_on("libpressio+hdf5", when="+hdf5")

    depends_on("boost")

    # 0.1.0 changed a bunch of things in the build system, make sure everything is up to date
    depends_on("libpressio@0.89.0:", when="@0.2.0:")
    depends_on("libpressio@0.88.0:", when="@0.1.6:")
    depends_on("libpressio@0.85.0:", when="@0.1.0:0.1.5")
    depends_on("libpressio-opt@0.13.3:", when="@0.1.0:+opt")
    depends_on("libpressio-errorinjector@0.7.0:", when="@0.1.0:+error_injector")
    depends_on("libpressio-tthresh@0.0.5:", when="@0.1.0:+tthresh")
    depends_on("libpressio-rmetric@0.0.4:", when="@0.1.0:+rcpp")
    depends_on("libpressio-adios2@0.0.2", when="@0.1.0:+adios2")

    depends_on("libpressio-opt", when="+opt")
    depends_on("libpressio-errorinjector", when="+error_injector")
    depends_on("libpressio-tthresh", when="+tthresh")
    depends_on("libpressio-rmetric", when="+rcpp")
    depends_on("libpressio-adios2", when="+adios2")
    depends_on("libpressio-sperr", when="+sperr")
    depends_on("libpressio-nvcomp", when="+nvcomp")

    variant("hdf5", default=True, description="support the hdf5 package")
    variant("opt", default=False, description="support the libpressio-opt package")
    variant(
        "error_injector", default=False, description="support the libpressio-errorinjector package"
    )
    variant("tthresh", default=False, description="depend on the GPL licensed libpressio-tthresh")
    variant("rcpp", default=False, description="depend on the GPL licensed libpressio-rmetric")
    variant("mpi", default=False, description="depend on MPI for distributed parallelism")
    variant("adios2", default=False, description="depend on ADIOS2 for IO modules")
    variant("sperr", default=False, description="depend on sperr", when="@0.1.2:")
    variant("nvcomp", default=False, description="depend on nvcomp", when="@0.1.0:")
    conflicts("+opt", "~mpi")

    def cmake_args(self):
        args = []
        if "+mpi" in self.spec:
            args.append("-DLIBPRESSIO_TOOLS_HAS_MPI=YES")
        if "+opt" in self.spec:
            args.append("-DLIBPRESSIO_TOOLS_HAS_OPT=YES")
        if "+error_injector" in self.spec:
            args.append("-DLIBPRESSIO_TOOLS_HAS_ERROR_INJECTOR=YES")
        if "+tthresh" in self.spec:
            args.append("-DLIBPRESSIO_TOOLS_HAS_TTHRESH=YES")
        if "+rcpp" in self.spec:
            args.append("-DLIBPRESSIO_TOOLS_HAS_RMETRIC=YES")
        if "+sperr" in self.spec:
            args.append("-DLIBPRESSIO_TOOLS_HAS_SPERR=YES")
        if "+nvcomp" in self.spec:
            args.append("-DLIBPRESSIO_TOOLS_HAS_NVCOMP=YES")
        if self.run_tests:
            args.append("-DBUILD_TESTING=ON")
        else:
            args.append("-DBUILD_TESTING=OFF")

        return args

    @run_after("build")
    @on_package_attributes(run_tests=True)
    def test(self):
        make("test")

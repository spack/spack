# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libxc(AutotoolsPackage, CudaPackage):
    """Libxc is a library of exchange-correlation functionals for
    density-functional theory."""

    homepage = "https://tddft.org/programs/libxc/"

    # The webserver at https://tddft.org/programs/libxc/download is unreliable,
    # see https://gitlab.com/libxc/libxc/-/issues/453. For the time being use
    # GitLab release tarballs.
    url = "https://gitlab.com/libxc/libxc/-/archive/6.1.0/libxc-6.1.0.tar.gz"

    version("6.1.0", sha256="f593745fa47ebfb9ddc467aaafdc2fa1275f0d7250c692ce9761389a90dd8eaf")
    version("6.0.0", sha256="0c774e8e195dd92800b9adf3df5f5721e29acfe9af4b191a9937c7de4f9aa9f6")
    version("5.2.3", sha256="38b60ed552b46367175b370e1ad5409fcf45c49b71ed13706a65b485f06a5417")
    version("5.1.7", sha256="1d50e1a92e59b5f3c8e7408f8612f0fb0e953d4f159515b7d81485891f3a1bbc")
    version("5.1.5", sha256="f2b428838536bcf2009af6a753f7314a069eed6a55bf1d1af4d4dcbcdd1c3697")
    version("5.1.3", sha256="53cbccae4227794c4f4e042d0c20c3171894d8eacd13fd78aab376d5971a966c")
    version("5.1.2", sha256="3fe05ccf7033622112f7d6ab28ac82301f5840b8d1bbe8b6df1022dbc732883f")
    version("5.1.0", sha256="5af77427c20a01d6d23ce769c8f40088b6bc7682c7b76cf1f87dae63605d5150")
    version("5.0.0", sha256="bfe8d8daa700d238bacf15ef2112f75e23d0a74c1a8d6c3e4741319561f577da")
    version("4.3.4", sha256="83aba38dfa03f34cc74f84c14c83bf501a43493c818c797e2d0682647569b147")
    version("4.3.2", sha256="e34700331aaffa5a3c421786863daf9a68cee4cbfbd2a79a4578fcf783205235")
    version("4.2.3", sha256="c68f5171828e5dd9ebdaa5c1a914f91a1456bbd18fc52041d92f662e790f6750")
    version("3.0.0", sha256="df2362351280edaf2233f3b2c8eb8e6dd6c68105f152897a4cc629fa346a7396")
    version("2.2.2", sha256="6ffaad40505dbe8f155049448554b54ea31d31babf74ccf6b7935bfe55eeafd8")
    version("2.2.1", sha256="c8577ba1ddd5c28fd0aa7c579ae65ab990eb7cb51ecf9f8175f9251f6deb9a06")

    variant("shared", default=True, description="Build shared libraries")

    conflicts("+shared +cuda", msg="Only ~shared supported with +cuda")
    conflicts("+cuda", when="@:4", msg="CUDA support only in libxc 5.0.0 and above")

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("perl", type="build")

    patch("0001-Bugfix-avoid-implicit-pointer-cast-to-make-libxc-com.patch", when="@5.0.0")
    patch("0002-Mark-xc_erfcx-a-GPU_FUNCTION.patch", when="@5.0.0")
    patch(
        "https://raw.githubusercontent.com/cp2k/cp2k/d9e473979eaef93bf16d7abafb9f21845af16eb8/tools/toolchain/scripts/stage3/libxc-6.0.0_mgga_xc_b97mv.patch",
        sha256="938113a697ee14988ccff153e1a8287fdb78072adc4f388a0af434261082fee5",
        when="@6.0.0",
    )

    patch("nvhpc-configure.patch", when="%nvhpc")
    patch("nvhpc-libtool.patch", when="@develop %nvhpc")

    @property
    def libs(self):
        """Libxc can be queried for the following parameters:

        - "static": returns the static library version of libxc
            (by default the shared version is returned)

        :return: list of matching libraries
        """
        query_parameters = self.spec.last_query.extra_parameters

        libraries = ["libxc"]

        # Libxc installs both shared and static libraries.
        # If a client ask for static explicitly then return
        # the static libraries
        shared = self.spec.variants["shared"].value and "static" not in query_parameters

        # Libxc has a fortran90 interface: give clients the
        # possibility to query for it
        if "fortran" in query_parameters:
            if self.version < Version("4.0.0"):
                libraries = ["libxcf90"] + libraries
            else:  # starting from version 4 there is also a stable f03 iface
                libraries = ["libxcf90", "libxcf03"] + libraries

        return find_libraries(libraries, root=self.prefix, shared=shared, recursive=True)

    def setup_build_environment(self, env):
        # microarchitecture-specific optimization flags should be controlled
        # by Spack, otherwise we may end up with contradictory or invalid flags
        # see https://github.com/spack/spack/issues/17794

        # https://gitlab.com/libxc/libxc/-/issues/430 (configure script does not ensure C99)
        # TODO: Switch to cmake since this is better supported
        env.append_flags("CFLAGS", self.compiler.c99_flag)
        if "%intel" in self.spec:
            if which("xiar"):
                env.set("AR", "xiar")

        if "%aocc" in self.spec:
            env.append_flags("FCFLAGS", "-fPIC")

        if "+cuda" in self.spec:
            nvcc = self.spec["cuda"].prefix.bin.nvcc
            env.set("CCLD", "{0} -ccbin {1}".format(nvcc, spack_cc))
            env.set("CC", "{0} -x cu -ccbin {1}".format(nvcc, spack_cc))

            cuda_arch = self.spec.variants["cuda_arch"].value[0]

            if cuda_arch != "none":
                env.append_flags("CFLAGS", "-arch=sm_{0}".format(cuda_arch))

    def configure_args(self):
        args = []
        args += self.enable_or_disable("shared")
        args += self.enable_or_disable("cuda")
        return args

    @run_after("configure")
    def patch_libtool(self):
        """AOCC support for LIBXC"""
        if "%aocc" in self.spec:
            filter_file(
                r"\$wl-soname \$wl\$soname",
                r"-fuse-ld=ld -Wl,-soname,\$soname",
                "libtool",
                string=True,
            )

    def check(self):
        # libxc provides a testsuite, but many tests fail
        # http://www.tddft.org/pipermail/libxc/2013-February/000032.html
        pass

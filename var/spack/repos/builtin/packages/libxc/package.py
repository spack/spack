# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libxc(AutotoolsPackage, CudaPackage):
    """Libxc is a library of exchange-correlation functionals for
    density-functional theory."""

    homepage = "https://tddft.org/programs/libxc/"
    url = "https://gitlab.com/libxc/libxc/-/archive/6.1.0/libxc-6.1.0.tar.gz"

    version("6.1.0", sha256="f593745fa47ebfb9ddc467aaafdc2fa1275f0d7250c692ce9761389a90dd8eaf")
    version("6.0.0", sha256="0c774e8e195dd92800b9adf3df5f5721e29acfe9af4b191a9937c7de4f9aa9f6")
    version("5.2.3", sha256="7b7a96d8eeb472c7b8cca7ac38eae27e0a8113ef44dae5359b0eb12592b4bcf2")
    version("5.1.7", sha256="1a818fdfe5c5f74270bc8ef0c59064e8feebcd66b8f642c08aecc1e7d125be34")
    version("5.1.5", sha256="02e4615a22dc3ec87a23efbd3d9be5bfad2445337140bad1720699571c45c3f9")
    version("5.1.3", sha256="0350defdd6c1b165e4cf19995f590eee6e0b9db95a6b221d28cecec40f4e85cd")
    version("5.1.2", sha256="180d52b5552921d1fac8a10869dd30708c0fb41dc202a3bbee0e36f43872718a")
    version("5.1.0", sha256="f67b6e518372871d9eed6e5dba77c3ab5ea030c229ba7a7d44bcf51f3258373f")
    version("5.0.0", sha256="1cdc57930f7b57da4eb9b2c55a50ba1c2c385936ddaf5582fee830994461a892")
    version("4.3.4", sha256="a8ee37ddc5079339854bd313272856c9d41a27802472ee9ae44b58ee9a298337")
    version("4.3.2", sha256="bc159aea2537521998c7fb1199789e1be71e04c4b7758d58282622e347603a6f")
    version("4.2.3", sha256="02e49e9ba7d21d18df17e9e57eae861e6ce05e65e966e1e832475aa09e344256")
    version("3.0.0", sha256="5542b99042c09b2925f2e3700d769cda4fb411b476d446c833ea28c6bfa8792a")
    version("2.2.2", sha256="6ca1d0bb5fdc341d59960707bc67f23ad54de8a6018e19e02eee2b16ea7cc642")
    version("2.2.1", sha256="ade61c1fa4ed238edd56408fd8ee6c2e305a3d5753e160017e2a71817c98fd00")

    variant("shared", default=True, description="Build shared libraries")

    conflicts("+shared +cuda", msg="Only ~shared supported with +cuda")
    conflicts("+cuda", when="@:4", msg="CUDA support only in libxc 5.0.0 and above")

    # Remove this when the release tarballs become available for 6.0.0 and above.
    with when("@6.0.0:"):
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

    def url_for_version(self, version):
        # The webserver at https://tddft.org/programs/libxc/download is unreliable,
        # see https://gitlab.com/libxc/libxc/-/issues/453. The pre 6.0.0 release tarballs
        # ar available in our source mirror, but the latest versions are not.
        if version < Version("6"):
            return f"https://www.tddft.org/programs/libxc/down/{version}/libxc-{version}.tar.gz"
        return f"https://gitlab.com/libxc/libxc/-/archive/{version}/libxc-{version}.tar.gz"

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

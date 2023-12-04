# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyScipy(PythonPackage):
    """Fundamental algorithms for scientific computing in Python."""

    homepage = "https://www.scipy.org/"
    pypi = "scipy/scipy-1.10.1.tar.gz"
    git = "https://github.com/scipy/scipy.git"

    maintainers("adamjstewart", "rgommers")

    version("main", branch="main")
    version("master", branch="master", deprecated=True)
    version("1.11.4", sha256="90a2b78e7f5733b9de748f589f09225013685f9b218275257f8a8168ededaeaa")
    version("1.11.3", sha256="bba4d955f54edd61899776bad459bf7326e14b9fa1c552181f0479cc60a568cd")
    version("1.11.2", sha256="b29318a5e39bd200ca4381d80b065cdf3076c7d7281c5e36569e99273867f61d")
    version("1.11.1", sha256="fb5b492fa035334fd249f0973cc79ecad8b09c604b42a127a677b45a9a3d4289")
    version("1.11.0", sha256="f9b0248cb9d08eead44cde47cbf6339f1e9aa0dfde28f5fb27950743e317bd5d")
    version("1.10.1", sha256="2cf9dfb80a7b4589ba4c40ce7588986d6d5cebc5457cad2c2880f6bc2d42f3a5")
    version("1.10.0", sha256="c8b3cbc636a87a89b770c6afc999baa6bcbb01691b5ccbbc1b1791c7c0a07540")
    version("1.9.3", sha256="fbc5c05c85c1a02be77b1ff591087c83bc44579c6d2bd9fb798bb64ea5e1a027")
    version("1.9.2", sha256="99e7720caefb8bca6ebf05c7d96078ed202881f61e0c68bd9e0f3e8097d6f794")
    version("1.9.1", sha256="26d28c468900e6d5fdb37d2812ab46db0ccd22c63baa095057871faa3a498bc9")
    version("1.9.0", sha256="c0dfd7d2429452e7e94904c6a3af63cbaa3cf51b348bd9d35b42db7e9ad42791")
    version("1.8.1", sha256="9e3fb1b0e896f14a85aa9a28d5f755daaeeb54c897b746df7a55ccb02b340f33")
    version("1.8.0", sha256="31d4f2d6b724bc9a98e527b5849b8a7e589bf1ea630c33aa563eda912c9ff0bd")
    version("1.7.3", sha256="ab5875facfdef77e0a47d5fd39ea178b58e60e454a4c85aa1e52fcb80db7babf")
    version("1.7.2", sha256="fa2dbabaaecdb502641b0b3c00dec05fb475ae48655c66da16c9ed24eda1e711")
    version("1.7.1", sha256="6b47d5fa7ea651054362561a28b1ccc8da9368a39514c1bbf6c0977a1c376764")
    version("1.7.0", sha256="998c5e6ea649489302de2c0bc026ed34284f531df89d2bdc8df3a0d44d165739")
    version("1.6.3", sha256="a75b014d3294fce26852a9d04ea27b5671d86736beb34acdfc05859246260707")
    version("1.6.2", sha256="e9da33e21c9bc1b92c20b5328adb13e5f193b924c9b969cd700c8908f315aa59")
    version("1.6.1", sha256="c4fceb864890b6168e79b0e714c585dbe2fd4222768ee90bc1aa0f8218691b11")
    version("1.6.0", sha256="cb6dc9f82dfd95f6b9032a8d7ea70efeeb15d5b5fd6ed4e8537bb3c673580566")
    version("1.5.4", sha256="4a453d5e5689de62e5d38edf40af3f17560bfd63c9c5bd228c18c1f99afa155b")
    version("1.5.3", sha256="ddae76784574cc4c172f3d5edd7308be16078dd3b977e8746860c76c195fa707")
    version("1.5.2", sha256="066c513d90eb3fd7567a9e150828d39111ebd88d3e924cdfc9f8ce19ab6f90c9")
    version("1.5.1", sha256="039572f0ca9578a466683558c5bf1e65d442860ec6e13307d528749cfe6d07b8")
    version("1.5.0", sha256="4ff72877d19b295ee7f7727615ea8238f2d59159df0bdd98f91754be4a2767f0")
    version("1.4.1", sha256="dee1bbf3a6c8f73b6b218cb28eed8dd13347ea2f87d572ce19b289d6fd3fbc59")
    version("1.4.0", sha256="31f7cfa93b01507c935c12b535e24812594002a02a56803d7cd063e9920d25e8")
    version("1.3.3", sha256="64bf4e8ae0db2d42b58477817f648d81e77f0b381d0ea4427385bba3f959380a")
    version("1.3.2", sha256="a03939b431994289f39373c57bbe452974a7da724ae7f9620a1beee575434da4")
    version("1.3.1", sha256="2643cfb46d97b7797d1dbdb6f3c23fe3402904e3c90e6facfe6a9b98d808c1b5")
    version("1.3.0", sha256="c3bb4bd2aca82fb498247deeac12265921fe231502a6bc6edea3ee7fe6c40a7a")
    version("1.2.3", sha256="ecbe6413ca90b8e19f8475bfa303ac001e81b04ec600d17fa7f816271f7cca57")
    version("1.2.2", sha256="a4331e0b8dab1ff75d2c67b5158a8bb9a83c799d7140094dda936d876c7cfbb1")
    version("1.2.1", sha256="e085d1babcb419bbe58e2e805ac61924dac4ca45a07c9fa081144739e500aa3c")
    version("1.1.0", sha256="878352408424dffaa695ffedf2f9f92844e116686923ed9aa8626fc30d32cfd1")

    # Based on wheel availability on PyPI
    depends_on("python@3.9:3.12", when="@1.11:", type=("build", "link", "run"))
    depends_on("python@3.8:3.11", when="@1.9.2:1.10", type=("build", "link", "run"))
    depends_on("python@3.8:3.10", when="@1.8:1.9.1", type=("build", "link", "run"))
    depends_on("python@:3.10", when="@1.7.2:1.7", type=("build", "link", "run"))
    depends_on("python@:3.9", when="@1.5.4:1.7.1", type=("build", "link", "run"))
    depends_on("python@:3.8", when="@1.3.2:1.5.3", type=("build", "link", "run"))
    depends_on("python@:3.7", when="@1.1:1.3.1", type=("build", "link", "run"))

    depends_on("py-meson-python@0.12.1:", when="@1.11:", type="build")
    depends_on("py-meson-python@0.11:", when="@1.10:", type="build")
    depends_on("py-meson-python@0.9:", when="@1.9.2:", type="build")
    depends_on("py-meson-python@0.8.1:", when="@1.9.1:", type="build")
    depends_on("py-meson-python@0.7:", when="@1.9:", type="build")
    depends_on("meson", when="@1.9.0:1.9.1", type="build")
    depends_on("py-cython@0.29.35:2", when="@1.11:", type="build")
    depends_on("py-cython@0.29.32:2", when="@1.9.2:", type="build")
    depends_on("py-cython@0.29.21:2", when="@1.9:", type="build")
    depends_on("py-cython@0.29.18:2", when="@1.7:", type="build")
    depends_on("py-pybind11@2.10.4:2.11.0", when="@1.11.3:", type=("build", "link"))
    depends_on("py-pybind11@2.10.4:2.10", when="@1.11.0:1.11.2", type=("build", "link"))
    depends_on("py-pybind11@2.10.1", when="@1.10", type=("build", "link"))
    depends_on("py-pybind11@2.4.3:2.10", when="@1.9.1:1.9", type=("build", "link"))
    depends_on("py-pybind11@2.4.3:2.9", when="@1.9.0", type=("build", "link"))
    depends_on("py-pybind11@2.4.3:2.8", when="@1.8", type=("build", "link"))
    depends_on("py-pybind11@2.4.3:2.7", when="@1.7.2:1.7", type=("build", "link"))
    depends_on("py-pybind11@2.4.3:2.6", when="@1.6.2:1.7.1", type=("build", "link"))
    depends_on("py-pybind11@2.4.3:", when="@1.5:1.6.1", type=("build", "link"))
    depends_on("py-pybind11@2.4.0:", when="@1.4.1:1.4", type=("build", "link"))
    depends_on("py-pybind11@2.2.4:", when="@1.4.0", type=("build", "link"))
    depends_on("py-pythran@0.12:", when="@1.10:", type="build")
    depends_on("py-pythran@0.10:", when="@1.8", type="build")
    depends_on("py-pythran@0.9.12:", when="@1.7.2:", type="build")
    depends_on("py-pythran@0.9.11:", when="@1.7:", type="build")
    depends_on("py-wheel@:0.40", when="@1.11.0:1.11.2", type="build")
    depends_on("py-wheel@:0.38", when="@1.10", type="build")
    depends_on("py-wheel@:0.37", when="@:1.9", type="build")
    depends_on("pkgconfig", when="@1.9:", type="build")
    depends_on("py-setuptools", when="@:1.8", type="build")
    depends_on("py-setuptools@:59", when="@1.8", type="build")
    depends_on("py-setuptools@:57", when="@1.7", type="build")
    depends_on("py-setuptools@:51.0.0", when="@1.6", type="build")
    depends_on("py-numpy@1.21.6:1.27", when="@1.11:", type=("build", "link", "run"))
    depends_on("py-numpy@1.19.5:1.26", when="@1.10", type=("build", "link", "run"))
    depends_on("py-numpy@1.18.5:1.25", when="@1.9", type=("build", "link", "run"))
    depends_on("py-numpy@1.17.3:1.24", when="@1.8", type=("build", "link", "run"))
    depends_on("py-numpy@1.16.5:1.22", when="@1.6:1.7", type=("build", "link", "run"))
    depends_on("py-numpy@1.14.5:1.21", when="@1.5", type=("build", "link", "run"))
    depends_on("py-numpy@1.13.3:1.21", when="@1.3:1.4", type=("build", "link", "run"))
    depends_on("py-numpy@1.8.2:1.20", when="@:1.2", type=("build", "link", "run"))
    depends_on("py-pytest", type="test")

    # Required to use --config-settings
    depends_on("py-pip@23.1:", when="@1.9:", type="build")

    # https://docs.scipy.org/doc/scipy/dev/toolchain.html#other-libraries
    depends_on("lapack@3.7.1:", when="@1.9:")
    depends_on("lapack@3.4.1:", when="@1.2:")
    depends_on("lapack")
    depends_on("blas")

    # meson.build
    # https://docs.scipy.org/doc/scipy/dev/toolchain.html#compilers
    conflicts("%gcc@:7", when="@1.10:", msg="SciPy requires GCC >= 8.0")
    conflicts("%gcc@:4.7", when="@:1.9", msg="SciPy requires GCC >= 4.8")
    conflicts(
        "%msvc@:19.19",
        when="@1.10:",
        msg="SciPy requires at least vc142 (default with Visual Studio 2019) "
        "when building with MSVC",
    )

    # https://github.com/scipy/scipy/issues/19352
    conflicts("^py-cython@3.0.3")

    # https://github.com/mesonbuild/meson/pull/10909#issuecomment-1282241479
    # Intel OneAPI ifx claims to support -fvisibility, but this does not work.
    # Meson adds this flag for all Python extensions which include Fortran code.
    conflicts("%oneapi@:2023.0", when="@1.9:")

    # error: expected unqualified-id (exact compiler versions unknown)
    conflicts("%apple-clang@15:", when="@:1.9")

    # https://docs.scipy.org/doc//scipy-1.10.1/release.1.7.3.html
    conflicts("platform=darwin target=aarch64:", when="@:1.7.2")

    # https://github.com/scipy/scipy/pull/11324
    conflicts("@1.4.0:1.4.1", when="target=ppc64le:")

    # https://github.com/scipy/scipy/issues/12860
    patch(
        "https://git.sagemath.org/sage.git/plain/build/pkgs/scipy/patches/extern_decls.patch?id=711fe05025795e44b84233e065d240859ccae5bd",
        sha256="5433f60831cb554101520a8f8871ac5a32c95f7a971ccd68b69049535b106780",
        when="@1.2:1.5.3",
    )

    patch("scipy-clang.patch", when="@1.5.0:1.6.3 %clang")

    @property
    def archive_files(self):
        return [join_path(self.stage.source_path, "build", "meson-logs", "meson-log.txt")]

    @run_before("install")
    def set_fortran_compiler(self):
        if self.compiler.f77 is None or self.compiler.fc is None:
            raise InstallError(
                "py-scipy requires Fortran compilers. Configure Fortran compiler to proceed."
            )

        if self.spec.satisfies("%fj"):
            with open("setup.cfg", "w") as f:
                f.write("[config_fc]\n")
                f.write("fcompiler = fujitsu\n")
        elif self.spec.satisfies("%intel") or self.spec.satisfies("%oneapi"):
            if self.spec.satisfies("target=x86:"):
                with open("setup.cfg", "w") as f:
                    f.write("[config_fc]\n")
                    f.write("fcompiler = intel\n")
            elif self.spec.satisfies("target=x86_64:"):
                with open("setup.cfg", "w") as f:
                    f.write("[config_fc]\n")
                    f.write("fcompiler = intelem\n")

    def setup_build_environment(self, env):
        # https://github.com/scipy/scipy/issues/9080
        env.set("F90", spack_fc)

        # https://github.com/scipy/scipy/issues/11611
        if self.spec.satisfies("@:1.4 %gcc@10:"):
            env.set("FFLAGS", "-fallow-argument-mismatch")
            if self.spec.satisfies("^py-numpy@1.16:1.17"):
                env.set("NPY_DISTUTILS_APPEND_FLAGS", "1")

        # https://github.com/scipy/scipy/issues/14935
        if self.spec.satisfies("%intel ^py-pythran"):
            env.set("SCIPY_USE_PYTHRAN", "0")

        # Pick up BLAS/LAPACK from numpy
        if self.spec.satisfies("@:1.8"):
            self.spec["py-numpy"].package.setup_build_environment(env)

        # https://github.com/scipy/scipy/issues/19357
        if self.spec.satisfies("%apple-clang@15:"):
            env.append_flags("LDFLAGS", "-Wl,-ld_classic")

    @when("@1.9:")
    def config_settings(self, spec, prefix):
        blas, lapack = self.spec["py-numpy"].package.blas_lapack_pkg_config()
        return {
            "builddir": "build",
            "compile-args": f"-j{make_jobs}",
            "setup-args": {
                # http://scipy.github.io/devdocs/building/blas_lapack.html
                "-Dblas": blas,
                "-Dlapack": lapack,
            },
        }

    @when("@:1.8")
    @run_before("install")
    def set_blas_lapack(self):
        self.spec["py-numpy"].package.blas_lapack_site_cfg()

    @run_after("install")
    @on_package_attributes(run_tests=True)
    def install_test(self):
        with working_dir("spack-test", create=True):
            python("-c", 'import scipy; scipy.test("full", verbose=2)')

# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import platform
import subprocess
from typing import Tuple

from spack.package import *


class PyNumpy(PythonPackage):
    """Fundamental package for array computing in Python."""

    homepage = "https://numpy.org/"
    pypi = "numpy/numpy-1.23.0.tar.gz"
    git = "https://github.com/numpy/numpy.git"

    maintainers("adamjstewart", "rgommers")

    version("main", branch="main")
    version("1.26.2", sha256="f65738447676ab5777f11e6bbbdb8ce11b785e105f690bc45966574816b6d3ea")
    version("1.26.1", sha256="c8c6c72d4a9f831f328efb1312642a1cafafaa88981d9ab76368d50d07d93cbe")
    version("1.26.0", sha256="f93fc78fe8bf15afe2b8d6b6499f1c73953169fad1e9a8dd086cdff3190e7fdf")
    version("1.25.2", sha256="fd608e19c8d7c55021dffd43bfe5492fab8cc105cc8986f813f8c3c048b38760")
    version("1.25.1", sha256="9a3a9f3a61480cc086117b426a8bd86869c213fc4072e606f01c4e4b66eb92bf")
    version("1.25.0", sha256="f1accae9a28dc3cda46a91de86acf69de0d1b5f4edd44a9b0c3ceb8036dfff19")
    version("1.24.4", sha256="80f5e3a4e498641401868df4208b74581206afbee7cf7b8329daae82676d9463")
    version("1.24.3", sha256="ab344f1bf21f140adab8e47fdbc7c35a477dc01408791f8ba00d018dd0bc5155")
    version("1.24.2", sha256="003a9f530e880cb2cd177cba1af7220b9aa42def9c4afc2a2fc3ee6be7eb2b22")
    version("1.24.1", sha256="2386da9a471cc00a1f47845e27d916d5ec5346ae9696e01a8a34760858fe9dd2")
    version("1.24.0", sha256="c4ab7c9711fe6b235e86487ca74c1b092a6dd59a3cb45b63241ea0a148501853")
    version("1.23.5", sha256="1b1766d6f397c18153d40015ddfc79ddb715cabadc04d2d228d4e5a8bc4ded1a")
    version("1.23.4", sha256="ed2cc92af0efad20198638c69bb0fc2870a58dabfba6eb722c933b48556c686c")
    version("1.23.3", sha256="51bf49c0cd1d52be0a240aa66f3458afc4b95d8993d2d04f0d91fa60c10af6cd")
    version("1.23.2", sha256="b78d00e48261fbbd04aa0d7427cf78d18401ee0abd89c7559bbf422e5b1c7d01")
    version("1.23.1", sha256="d748ef349bfef2e1194b59da37ed5a29c19ea8d7e6342019921ba2ba4fd8b624")
    version("1.23.0", sha256="bd3fa4fe2e38533d5336e1272fc4e765cabbbde144309ccee8675509d5cd7b05")
    version("1.22.4", sha256="425b390e4619f58d8526b3dcf656dde069133ae5c240229821f01b5f44ea07af")
    version("1.22.3", sha256="dbc7601a3b7472d559dc7b933b18b4b66f9aa7452c120e87dfb33d02008c8a18")
    version("1.22.2", sha256="076aee5a3763d41da6bef9565fdf3cb987606f567cd8b104aded2b38b7b47abf")
    version("1.22.1", sha256="e348ccf5bc5235fc405ab19d53bec215bb373300e5523c7b476cc0da8a5e9973")
    version("1.22.0", sha256="a955e4128ac36797aaffd49ab44ec74a71c11d6938df83b1285492d277db5397")
    version("1.21.6", sha256="ecb55251139706669fdec2ff073c98ef8e9a84473e51e716211b41aa0f18e656")
    version("1.21.5", sha256="6a5928bc6241264dce5ed509e66f33676fc97f464e7a919edc672fb5532221ee")
    version("1.21.4", sha256="e6c76a87633aa3fa16614b61ccedfae45b91df2767cf097aa9c933932a7ed1e0")
    version("1.21.3", sha256="63571bb7897a584ca3249c86dd01c10bcb5fe4296e3568b2e9c1a55356b6410e")
    version("1.21.2", sha256="423216d8afc5923b15df86037c6053bf030d15cc9e3224206ef868c2d63dd6dc")
    version("1.21.1", sha256="dff4af63638afcc57a3dfb9e4b26d434a7a602d225b42d746ea7fe2edf1342fd")
    version("1.21.0", sha256="e80fe25cba41c124d04c662f33f6364909b985f2eb5998aaa5ae4b9587242cce")
    version("1.20.3", sha256="e55185e51b18d788e49fe8305fd73ef4470596b33fc2c1ceb304566b99c71a69")
    version("1.20.2", sha256="878922bf5ad7550aa044aa9301d417e2d3ae50f0f577de92051d739ac6096cee")
    version("1.20.1", sha256="3bc63486a870294683980d76ec1e3efc786295ae00128f9ea38e2c6e74d5a60a")
    version("1.20.0", sha256="3d8233c03f116d068d5365fed4477f2947c7229582dad81e5953088989294cec")
    version("1.19.5", sha256="a76f502430dd98d7546e1ea2250a7360c065a5fdea52b2dffe8ae7180909b6f4")
    version("1.19.4", sha256="141ec3a3300ab89c7f2b0775289954d193cc8edb621ea05f99db9cb181530512")
    version("1.19.3", sha256="35bf5316af8dc7c7db1ad45bec603e5fb28671beb98ebd1d65e8059efcfd3b72")
    version("1.19.2", sha256="0d310730e1e793527065ad7dde736197b705d0e4c9999775f212b03c44a8484c")
    version("1.19.1", sha256="b8456987b637232602ceb4d663cb34106f7eb780e247d51a260b84760fd8f491")
    version("1.19.0", sha256="76766cc80d6128750075378d3bb7812cf146415bd29b588616f72c943c00d598")
    version("1.18.5", sha256="34e96e9dae65c4839bd80012023aadd6ee2ccb73ce7fdf3074c62f301e63120b")
    version("1.18.4", sha256="bbcc85aaf4cd84ba057decaead058f43191cc0e30d6bc5d44fe336dc3d3f4509")
    version("1.18.3", sha256="e46e2384209c91996d5ec16744234d1c906ab79a701ce1a26155c9ec890b8dc8")
    version("1.18.2", sha256="e7894793e6e8540dbeac77c87b489e331947813511108ae097f1715c018b8f3d")
    version("1.18.1", sha256="b6ff59cee96b454516e47e7721098e6ceebef435e3e21ac2d6c3b8b02628eb77")
    version("1.18.0", sha256="a9d72d9abaf65628f0f31bbb573b7d9304e43b1e6bbae43149c17737a42764c4")
    version("1.17.5", sha256="16507ba6617f62ae3c6ab1725ae6f550331025d4d9a369b83f6d5a470446c342")
    version("1.17.4", sha256="f58913e9227400f1395c7b800503ebfdb0772f1c33ff8cb4d6451c06cabdf316")
    version("1.17.3", sha256="a0678793096205a4d784bd99f32803ba8100f639cf3b932dc63b21621390ea7e")
    version("1.17.2", sha256="73615d3edc84dd7c4aeb212fa3748fb83217e00d201875a47327f55363cef2df")
    version("1.17.1", sha256="f11331530f0eff69a758d62c2461cd98cdc2eae0147279d8fc86e0464eb7e8ca")
    version("1.17.0", sha256="951fefe2fb73f84c620bec4e001e80a80ddaa1b84dce244ded7f1e0cbe0ed34a")
    version("1.16.6", sha256="e5cf3fdf13401885e8eea8170624ec96225e2174eb0c611c6f26dd33b489e3ff")
    version("1.16.5", sha256="8bb452d94e964b312205b0de1238dd7209da452343653ab214b5d681780e7a0c")
    version("1.16.4", sha256="7242be12a58fec245ee9734e625964b97cf7e3f2f7d016603f9e56660ce479c7")
    version("1.16.3", sha256="78a6f89da87eeb48014ec652a65c4ffde370c036d780a995edaeb121d3625621")
    version("1.16.2", sha256="6c692e3879dde0b67a9dc78f9bfb6f61c666b4562fd8619632d7043fb5b691b0")
    version("1.16.1", sha256="31d3fe5b673e99d33d70cfee2ea8fe8dccd60f265c3ed990873a88647e3dd288")
    version("1.16.0", sha256="cb189bd98b2e7ac02df389b6212846ab20661f4bafe16b5a70a6f1728c1cc7cb")
    version("1.15.4", sha256="3d734559db35aa3697dadcea492a423118c5c55d176da2f3be9c98d4803fc2a7")
    version("1.15.3", sha256="1c0c80e74759fa4942298044274f2c11b08c86230b25b8b819e55e644f5ff2b6")
    version("1.15.2", sha256="27a0d018f608a3fe34ac5e2b876f4c23c47e38295c47dd0775cc294cd2614bc1")
    version("1.15.2", sha256="27a0d018f608a3fe34ac5e2b876f4c23c47e38295c47dd0775cc294cd2614bc1")
    version("1.15.1", sha256="7b9e37f194f8bcdca8e9e6af92e2cbad79e360542effc2dd6b98d63955d8d8a3")
    version("1.15.0", sha256="f28e73cf18d37a413f7d5de35d024e6b98f14566a10d82100f9dc491a7d449f9")
    version("1.14.6", sha256="1250edf6f6c43e1d7823f0967416bc18258bb271dc536298eb0ea00a9e45b80a")
    version("1.14.5", sha256="a4a433b3a264dbc9aa9c7c241e87c0358a503ea6394f8737df1683c7c9a102ac")

    depends_on("python@3.9:3.12", when="@1.26:", type=("build", "link", "run"))
    depends_on("python@3.9:3.11", when="@1.25", type=("build", "link", "run"))
    depends_on("python@3.8:3.11", when="@1.23.2:1.24", type=("build", "link", "run"))
    depends_on("python@3.8:3.10", when="@1.22:1.23.1", type=("build", "link", "run"))
    depends_on("python@:3.10", when="@1.21.2:1.21", type=("build", "link", "run"))
    depends_on("python@:3.9", when="@1.19.3:1.21.1", type=("build", "link", "run"))
    depends_on("python@:3.8", when="@1.17.3:1.19.2", type=("build", "link", "run"))
    depends_on("python@:3.7", when="@1.14.5:1.17.2", type=("build", "link", "run"))

    depends_on("py-cython@0.29.34:3", when="@1.26:", type="build")
    depends_on("py-cython@0.29.34:2", when="@1.25", type="build")
    depends_on("py-cython@0.29.30:2", when="@1.22.4:1.24", type="build")
    depends_on("py-cython@0.29.24:2", when="@1.21.2:1.22.3", type="build")
    depends_on("py-cython@0.29.21:2", when="@1.19.1:1.21.1", type="build")
    depends_on("py-cython@0.29.14:2", when="@1.18.1:1.19.0", type="build")
    depends_on("py-cython@0.29.13:2", when="@1.18.0", type="build")
    depends_on("py-pyproject-metadata@0.7.1:", when="@1.26:", type="build")
    depends_on("py-tomli@1:", when="@1.26: ^python@:3.10", type="build")
    depends_on("py-setuptools@60:", when="@1.26: ^python@3.12:", type="build")
    # https://github.com/spack/spack/pull/32078
    depends_on("py-setuptools@:63", when="@:1.25", type=("build", "run"))
    depends_on("py-setuptools@:59", when="@:1.22.1", type=("build", "run"))
    depends_on("py-colorama", when="@1.26: platform=windows", type="build")

    # Required to use --config-settings
    depends_on("py-pip@23.1:", when="@1.26:", type="build")
    # meson is vendored, ninja and pkgconfig are not
    depends_on("ninja@1.8.2:", when="@1.26:", type="build")
    depends_on("pkgconfig", when="@1.26:", type="build")
    depends_on("blas")
    depends_on("lapack")

    # test_requirements.txt
    depends_on("py-nose@1.0.0:", when="@:1.14", type="test")
    depends_on("py-pytest", when="@1.15:", type="test")
    depends_on("py-hypothesis", when="@1.19:", type="test")
    depends_on("py-typing-extensions@4.2:", when="@1.23:", type="test")

    # Allows you to specify order of BLAS/LAPACK preference
    # https://github.com/numpy/numpy/pull/13132
    patch("blas-lapack-order.patch", when="@1.15:1.16")

    # Add Fujitsu Fortran compiler
    patch("add_fj_compiler.patch", when="@1.19.3:1.19.5%fj")
    patch("add_fj_compiler2.patch", when="@1.19.0:1.19.2%fj")
    patch("add_fj_compiler3.patch", when="@1.14.0:1.18.5%fj")

    patch("check_executables.patch", when="@1.20.0:")
    patch("check_executables2.patch", when="@1.19.0:1.19.5")
    patch("check_executables3.patch", when="@1.16.0:1.18.5")
    patch("check_executables4.patch", when="@1.14.0:1.15.4")

    # Backport bug fix for f2py's define for threading when building with Mingw
    patch(
        "https://github.com/numpy/numpy/pull/20881.patch?full_index=1",
        sha256="802970a9034d40a8a8f49a03f489d5361d5eabf69249621e6757651448910f1a",
        when="@1.20.3:1.22.1",
    )
    # Patch to update compiler flags.
    # See https://github.com/spack/spack/issues/30373
    patch(
        "https://github.com/numpy/numpy/pull/21448.patch?full_index=1",
        sha256="e9508c3b3a1e1a24669014a0c1b9f3b009a149ea3886cf711eaef2a32b247fdb",
        when="@1.22.0:1.22.3",
    )

    # meson.build
    # https://docs.scipy.org/doc/scipy/dev/toolchain.html#compilers
    conflicts("%gcc@:8.3", when="@1.26:", msg="NumPy requires GCC >= 8.4")
    conflicts("%gcc@:4.7", msg="NumPy requires GCC >= 4.8")
    conflicts(
        "%msvc@:19.19",
        when="@1.26:",
        msg="NumPy requires at least vc142 (default with Visual Studio 2019) "
        "when building with MSVC",
    )

    # version 1.21.0 runs into an infinite loop during printing
    # (e.g. print(numpy.ones(1000)) when compiled with gcc 11
    conflicts("%gcc@11:", when="@1.21.0")

    # NVHPC support added in https://github.com/numpy/numpy/pull/17344
    conflicts("%nvhpc", when="@:1.19")

    # See https://github.com/numpy/numpy/issues/22011
    conflicts("%intel", when="@1.23.0:1.23.3")
    conflicts("%oneapi", when="@1.23.0:1.23.3")

    @property
    def archive_files(self):
        return [join_path(self.stage.source_path, "build", "meson-logs", "meson-log.txt")]

    def url_for_version(self, version):
        url = "https://files.pythonhosted.org/packages/source/n/numpy/numpy-{}.{}"
        if version >= Version("1.23"):
            ext = "tar.gz"
        else:
            ext = "zip"
        return url.format(version, ext)

    def flag_handler(self, name, flags):
        # -std=c99 at least required, old versions of GCC default to -std=c90
        if self.spec.satisfies("%gcc@:5.1") and name == "cflags":
            flags.append(self.compiler.c99_flag)
        # Check gcc version in use by intel compiler
        # This will essentially check the system gcc compiler unless a gcc
        # module is already loaded.
        if self.spec.satisfies("%intel") and name == "cflags":
            p1 = subprocess.Popen([self.compiler.cc, "-v"], stderr=subprocess.PIPE)
            p2 = subprocess.Popen(
                ["grep", "compatibility"], stdin=p1.stderr, stdout=subprocess.PIPE
            )
            p1.stderr.close()
            out, err = p2.communicate()
            gcc_version = Version(out.split()[5].decode("utf-8"))
            if gcc_version < Version("4.8"):
                raise InstallError(
                    "The GCC version that the Intel compiler "
                    "uses must be >= 4.8. The GCC in use is "
                    "{0}".format(gcc_version)
                )
            if gcc_version <= Version("5.1"):
                flags.append(self.compiler.c99_flag)

        return (flags, None, None)

    def blas_lapack_pkg_config(self) -> Tuple[str, str]:
        """Convert library names to pkg-config names.

        Returns:
            The names of the blas and lapack libs that pkg-config should search for.
        """
        spec = self.spec
        blas = spec["blas"].libs.names[0]
        lapack = spec["lapack"].libs.names[0]

        if spec["blas"].name in ["intel-mkl", "intel-parallel-studio", "intel-oneapi-mkl"]:
            blas = "mkl-dynamic-lp64-seq"

        if spec["lapack"].name in ["intel-mkl", "intel-parallel-studio", "intel-oneapi-mkl"]:
            lapack = "mkl-dynamic-lp64-seq"

        if spec["blas"].name in ["blis", "amdblis"]:
            blas = "blis"

        if spec["blas"].name == "cray-libsci":
            blas = "libsci"

        if spec["lapack"].name == "cray-libsci":
            lapack = "libsci"

        if "armpl" in blas:
            if "_mp" in blas:
                blas = "armpl-dynamic-lp64-omp"
            else:
                blas = "armpl-dynamic-lp64-seq"

        if "armpl" in lapack:
            if "_mp" in lapack:
                lapack = "armpl-dynamic-lp64-omp"
            else:
                lapack = "armpl-dynamic-lp64-seq"

        return blas, lapack

    @when("@1.26:")
    def config_settings(self, spec, prefix):
        blas, lapack = self.blas_lapack_pkg_config()
        return {
            "builddir": "build",
            "compile-args": f"-j{make_jobs}",
            "setup-args": {
                # https://scipy.github.io/devdocs/building/blas_lapack.html
                "-Dblas": blas,
                "-Dlapack": lapack,
                # https://numpy.org/doc/stable/reference/simd/build-options.html
                # TODO: get this working in CI
                # "-Dcpu-baseline": "native",
                # "-Dcpu-dispatch": "none",
            },
        }

    def blas_lapack_site_cfg(self) -> None:
        """Write a site.cfg file to configure BLAS/LAPACK."""
        spec = self.spec

        # https://numpy.org/doc/1.25/user/building.html
        # https://github.com/numpy/numpy/blob/v1.25.2/site.cfg.example
        def write_library_dirs(f, dirs):
            f.write("library_dirs = {0}\n".format(dirs))
            if not (
                (platform.system() == "Darwin")
                and (Version(platform.mac_ver()[0]).up_to(2) == Version("10.12"))
            ):
                f.write("rpath = {0}\n".format(dirs))

        blas_libs = spec["blas"].libs
        blas_headers = spec["blas"].headers

        lapack_libs = spec["lapack"].libs
        lapack_headers = spec["lapack"].headers

        lapackblas_libs = lapack_libs + blas_libs
        lapackblas_headers = lapack_headers + blas_headers

        blas_lib_names = ",".join(blas_libs.names)
        blas_lib_dirs = ":".join(blas_libs.directories)
        blas_header_dirs = ":".join(blas_headers.directories)

        lapack_lib_names = ",".join(lapack_libs.names)
        lapack_lib_dirs = ":".join(lapack_libs.directories)
        lapack_header_dirs = ":".join(lapack_headers.directories)

        lapackblas_lib_names = ",".join(lapackblas_libs.names)
        lapackblas_lib_dirs = ":".join(lapackblas_libs.directories)
        lapackblas_header_dirs = ":".join(lapackblas_headers.directories)

        # Tell numpy where to find BLAS/LAPACK libraries
        with open("site.cfg", "w") as f:
            if (
                "^intel-mkl" in spec
                or "^intel-parallel-studio+mkl" in spec
                or "^intel-oneapi-mkl" in spec
            ):
                f.write("[mkl]\n")
                # FIXME: as of @1.11.2, numpy does not work with separately
                # specified threading and interface layers. A workaround is a
                # terribly bad idea to use mkl_rt. In this case Spack will no
                # longer be able to guarantee that one and the same variant of
                # Blas/Lapack (32/64bit, threaded/serial) is used within the
                # DAG. This may lead to a lot of hard-to-debug segmentation
                # faults on user's side. Users may also break working
                # installation by (unconsciously) setting environment variable
                # to switch between different interface and threading layers
                # dynamically. From this perspective it is no different from
                # throwing away RPATH's and using LD_LIBRARY_PATH throughout
                # Spack.
                f.write("libraries = {0}\n".format("mkl_rt"))
                write_library_dirs(f, lapackblas_lib_dirs)
                f.write("include_dirs = {0}\n".format(lapackblas_header_dirs))

            if "^blis" in spec or "^amdblis" in spec:
                f.write("[blis]\n")
                f.write("libraries = {0}\n".format(blas_lib_names))
                write_library_dirs(f, blas_lib_dirs)
                f.write("include_dirs = {0}\n".format(blas_header_dirs))

            if "^openblas" in spec:
                f.write("[openblas]\n")
                f.write("libraries = {0}\n".format(lapackblas_lib_names))
                write_library_dirs(f, lapackblas_lib_dirs)
                f.write("include_dirs = {0}\n".format(lapackblas_header_dirs))
                symbol_suffix = spec["openblas"].variants["symbol_suffix"].value
                if symbol_suffix != "none":
                    f.write("symbol_suffix = {0}\n".format(symbol_suffix))

            if "^libflame" in spec or "^amdlibflame" in spec:
                f.write("[flame]\n")
                f.write("libraries = {0}\n".format(lapack_lib_names))
                write_library_dirs(f, lapack_lib_dirs)
                f.write("include_dirs = {0}\n".format(lapack_header_dirs))

            if "^atlas" in spec:
                f.write("[atlas]\n")
                f.write("libraries = {0}\n".format(lapackblas_lib_names))
                write_library_dirs(f, lapackblas_lib_dirs)
                f.write("include_dirs = {0}\n".format(lapackblas_header_dirs))

            if "^veclibfort" in spec:
                f.write("[accelerate]\n")
                f.write("libraries = {0}\n".format(lapackblas_lib_names))
                write_library_dirs(f, lapackblas_lib_dirs)

            if "^netlib-lapack" in spec or "^cray-libsci" in spec:
                # netlib and Cray require blas and lapack listed
                # separately so that scipy can find them
                if spec.satisfies("+blas"):
                    f.write("[blas]\n")
                    f.write("libraries = {0}\n".format(blas_lib_names))
                    write_library_dirs(f, blas_lib_dirs)
                    f.write("include_dirs = {0}\n".format(blas_header_dirs))
                if spec.satisfies("+lapack"):
                    f.write("[lapack]\n")
                    f.write("libraries = {0}\n".format(lapack_lib_names))
                    write_library_dirs(f, lapack_lib_dirs)
                    f.write("include_dirs = {0}\n".format(lapack_header_dirs))

            if "^fujitsu-ssl2" in spec:
                if spec.satisfies("+blas"):
                    f.write("[blas]\n")
                    f.write("libraries = {0}\n".format(spec["blas"].libs.names[0]))
                    write_library_dirs(f, blas_lib_dirs)
                    f.write("include_dirs = {0}\n".format(blas_header_dirs))
                    f.write("extra_link_args = {0}\n".format(self.spec["blas"].libs.ld_flags))
                if spec.satisfies("+lapack"):
                    f.write("[lapack]\n")
                    f.write("libraries = {0}\n".format(spec["lapack"].libs.names[0]))
                    write_library_dirs(f, lapack_lib_dirs)
                    f.write("include_dirs = {0}\n".format(lapack_header_dirs))
                    f.write("extra_link_args = {0}\n".format(self.spec["lapack"].libs.ld_flags))

            if "^armpl-gcc" in spec or "^acfl" in spec:
                if spec.satisfies("+blas"):
                    f.write("[blas]\n")
                    f.write("libraries = {0}\n".format(blas_lib_names))
                    write_library_dirs(f, blas_lib_dirs)
                    f.write("include_dirs = {0}\n".format(blas_header_dirs))
                if spec.satisfies("+lapack"):
                    f.write("[lapack]\n")
                    f.write("libraries = {0}\n".format(lapack_lib_names))
                    write_library_dirs(f, lapack_lib_dirs)
                    f.write("include_dirs = {0}\n".format(lapack_header_dirs))

    @when("@:1.25")
    @run_before("install")
    def set_blas_lapack(self):
        self.blas_lapack_site_cfg()

    @when("@1.26:")
    def setup_build_environment(self, env):
        # https://github.com/scipy/scipy/issues/19357
        if self.spec.satisfies("%apple-clang@15:"):
            env.append_flags("LDFLAGS", "-Wl,-ld_classic")

    @when("@:1.25")
    def setup_build_environment(self, env):
        # Tell numpy which BLAS/LAPACK libraries we want to use.
        spec = self.spec
        # https://github.com/numpy/numpy/pull/13132
        # https://numpy.org/doc/1.25/user/building.html#accelerated-blas-lapack-libraries
        # https://numpy.org/doc/1.25/user/building.html#blas
        if (
            spec["blas"].name == "intel-mkl"
            or spec["blas"].name == "intel-parallel-studio"
            or spec["blas"].name == "intel-oneapi-mkl"
        ):
            blas = "mkl"
        elif spec["blas"].name == "blis" or spec["blas"].name == "amdblis":
            blas = "blis"
        elif spec["blas"].name == "openblas":
            blas = "openblas"
        elif spec["blas"].name == "atlas":
            blas = "atlas"
        elif spec["blas"].name == "veclibfort":
            blas = "accelerate"
        else:
            blas = "blas"

        env.set("NPY_BLAS_ORDER", blas)

        # https://numpy.org/doc/1.25/user/building.html#lapack
        if (
            spec["lapack"].name == "intel-mkl"
            or spec["lapack"].name == "intel-parallel-studio"
            or spec["lapack"].name == "intel-oneapi-mkl"
        ):
            lapack = "mkl"
        elif spec["lapack"].name == "openblas":
            lapack = "openblas"
        elif spec["lapack"].name == "libflame" or spec["lapack"].name == "amdlibflame":
            lapack = "flame"
        elif spec["lapack"].name == "atlas":
            lapack = "atlas"
        elif spec["lapack"].name == "veclibfort":
            lapack = "accelerate"
        else:
            lapack = "lapack"

        env.set("NPY_LAPACK_ORDER", lapack)

    @run_after("install")
    @on_package_attributes(run_tests=True)
    def install_test(self):
        with working_dir("spack-test", create=True):
            python("-c", 'import numpy; numpy.test("full", verbose=2)')

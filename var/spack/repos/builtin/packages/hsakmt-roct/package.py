# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import os

from spack.package import *


class HsakmtRoct(CMakePackage):
    """This is a thunk python recipe to build and install Thunk Interface.
    Thunk Interface is a user-mode API interfaces used to interact
    with the ROCk driver."""

    homepage = "https://github.com/RadeonOpenCompute/ROCT-Thunk-Interface"
    git = "https://github.com/RadeonOpenCompute/ROCT-Thunk-Interface.git"
    url = "https://github.com/RadeonOpenCompute/ROCT-Thunk-Interface/archive/rocm-5.5.0.tar.gz"
    tags = ["rocm"]

    maintainers("srekolam", "renjithravindrankannath")

    version("master", branch="master")
    version("5.6.1", sha256="d60b355bfd21a08e0e36270fd56f98d052c3c6edca47da887fa32bf32759c29b")
    version("5.6.0", sha256="cd009c5c09f664f046c428ba9843582ab468f7b88d560747eb949d8d7f8c5567")
    version("5.5.1", sha256="4ffde3fc1f91f24cdbf09263fd8e012a3995ad10854f4c1d866beab7b9f36bf4")
    version("5.5.0", sha256="2b11fd8937c2b06cd4ddea2c3699fbf3d1651892c4c5957d38553b993dd9af18")
    version("5.4.3", sha256="3799abbe7177fbff3b304e2a363e2b39e8864f8650ae569b2b88b9291f9a710c")
    version("5.4.0", sha256="690a78a6e67ae2b3f518dbc4a1e267237d6a342e1063b31eef297f4a04d780f8")
    version("5.3.3", sha256="b5350de915997ed48072b37a21c2c44438028255f6cc147c25a196ad383c52e7")
    version("5.3.0", sha256="c150be3958fd46e57bfc9db187819ec34b1db8f0cf9b69f8c3f8915001800ab8")
    version("5.2.3", sha256="8d313b8fd945a8d7248c00a2de9a2ee896fe77e464430a91b63400a986ec0bf0")
    version("5.2.1", sha256="13c4a6748c4ae70f87869f10fda101d67c9dbaecf040687f7f5d9bb8b6d0506c")
    version("5.2.0", sha256="3797cb0eafbec3fd3d4a2b53f789eb8cdbab30729f13dbcca0a10bc1bafd2187")
    version("5.1.3", sha256="3c66b1aa7451571ce8bee10e601d34b93c9416b9be476610ee5685dbad81034a")
    version("5.1.0", sha256="032717e80b1aefed59f11399e575564ee86ee7c125e889f7c79c2afdfab1eb93")
    version(
        "5.0.2",
        sha256="f2a27ac18aada1dc0dba6455beb7dd7d88a4457c1917024ea372fecb03356e97",
        deprecated=True,
    )
    version(
        "5.0.0",
        sha256="1d803572eac0d6186260b5671268bad7513aa9433f9c2e99f14c8bf766c02122",
        deprecated=True,
    )
    version(
        "4.5.2",
        sha256="fb8e44226b9e393baf51bfcb9873f63ce7e4fcf7ee7f530979cf51857ea4d24b",
        deprecated=True,
    )
    version(
        "4.5.0",
        sha256="620b39959e0ee5d709b8cf6eb3cc06c8356d72838343756230c638899b10bb9a",
        deprecated=True,
    )
    version(
        "4.3.1",
        sha256="9d0727e746d4ae6e2709e3534d91046640be511a71c027f47db25e529fe3b4d4",
        deprecated=True,
    )
    version(
        "4.3.0",
        sha256="1ef5fe687bc23ffda17841fe354c1fb94e9aaf276ca9e5757488852f9066f231",
        deprecated=True,
    )
    version(
        "4.2.0",
        sha256="cc325d4b9a96062f2ad0515fce724a8c64ba56a7d7f1ac4a0753941b8599c52e",
        deprecated=True,
    )
    version(
        "4.1.0",
        sha256="8443ed5907a7ba9ad4003a49d90ff7b8886e1b2a5e90f14e4035765a7f64d7ca",
        deprecated=True,
    )
    version(
        "4.0.0",
        sha256="a6960fffc8388731ee18953faae12d1449c582e3b3594418845a544455895f42",
        deprecated=True,
    )
    version(
        "3.10.0",
        sha256="a3d629247a763cc36f5d48e9122cee8498574af628e14e3c38686c05f66e3e06",
        deprecated=True,
    )
    version(
        "3.9.0",
        sha256="e1bb8b010855736d8a97957222f648532d42646ec2964776a9a1455dc81104a3",
        deprecated=True,
    )
    version(
        "3.8.0",
        sha256="cd5440f31f592737b5d05448704bd01f91f73cfcab8a7829922e81332575cfe8",
        deprecated=True,
    )
    version(
        "3.7.0",
        sha256="b357fe7f425996c49f41748923ded1a140933de7564a70a828ed6ded6d896458",
        deprecated=True,
    )
    version(
        "3.5.0",
        sha256="d9f458c16cb62c3c611328fd2f2ba3615da81e45f3b526e45ff43ab4a67ee4aa",
        deprecated=True,
    )

    variant("shared", default=True, description="Build shared or static library")

    depends_on("pkgconfig", type="build", when="@4.5.0:")
    depends_on("cmake@3:", type="build")
    depends_on("numactl")
    depends_on("libdrm", when="@4.5.0:")

    for ver in ["5.3.0", "5.4.0", "5.4.3"]:
        depends_on("llvm-amdgpu@" + ver, type="test", when="@" + ver)

    for ver in ["5.5.0", "5.5.1", "5.6.0", "5.6.1"]:
        depends_on("rocm-core@" + ver, when="@" + ver)
        depends_on("llvm-amdgpu@" + ver, type="test", when="@" + ver)

    # See https://github.com/RadeonOpenCompute/ROCT-Thunk-Interface/issues/72
    # and https://github.com/spack/spack/issues/28398
    patch("0001-Remove-compiler-support-libraries-and-libudev-as-req.patch", when="@4.5.0:5.2")
    patch("0002-Remove-compiler-support-libraries-and-libudev-as-req-5.3.patch", when="@5.3.0:5.4")

    @property
    def install_targets(self):
        if self.version == Version("3.5.0"):
            return ["install", "install-dev"]
        else:
            return ["install"]

    def cmake_args(self):
        args = []
        if self.spec.satisfies("@:5.4.3"):
            args.append(self.define_from_variant("BUILD_SHARED_LIBS", "shared"))
        else:
            args.append(self.define("BUILD_SHARED_LIBS", False))
        if self.spec.satisfies("@5.4.3:"):
            args.append("-DCMAKE_INSTALL_LIBDIR=lib")
        return args

    @run_after("install")
    @on_package_attributes(run_tests=True)
    def check_install(self):
        if self.spec.satisfies("@:5.3.0"):
            print("Skipping: stand-alone tests")
            return
        test_dir = "tests/kfdtest"
        with working_dir(test_dir, create=True):
            cmake_bin = join_path(self.spec["cmake"].prefix.bin, "cmake")
            prefixes = ";".join(
                [
                    self.spec["libdrm"].prefix,
                    self.spec["hsakmt-roct"].prefix,
                    self.spec["numactl"].prefix,
                    self.spec["pkgconfig"].prefix,
                    self.spec["llvm-amdgpu"].prefix,
                    self.spec["zlib-api"].prefix,
                    self.spec["ncurses"].prefix,
                ]
            )
            hsakmt_path = ";".join([self.spec["hsakmt-roct"].prefix])
            cc_options = [
                "-DCMAKE_PREFIX_PATH=" + prefixes,
                "-DLIBHSAKMT_PATH=" + hsakmt_path,
                ".",
            ]
            self.run_test(cmake_bin, cc_options)
            make()
            os.environ["LD_LIBRARY_PATH"] = hsakmt_path
            os.environ["BIN_DIR"] = os.getcwd()
            self.run_test("scripts/run_kfdtest.sh")
            make("clean")

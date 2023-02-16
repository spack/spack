# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re

from spack.package import *


class Hipsolver(CMakePackage):
    """hipSOLVER is a LAPACK marshalling library, with multiple supported backends.
    It sits between the application and a 'worker' LAPACK library, marshalling
    inputs into the backend library and marshalling results back to the application.
    hipSOLVER exports an interface that does not require the client to change,
    regardless of the chosen backend. Currently, hipSOLVER supports rocSOLVER
    and cuSOLVER as backends."""

    homepage = "https://github.com/ROCmSoftwarePlatform/hipSOLVER"
    git = "https://github.com/ROCmSoftwarePlatform/hipSOLVER.git"
    url = "https://github.com/ROCmSoftwarePlatform/hipSOLVER/archive/rocm-5.4.3.tar.gz"
    tags = ["rocm"]

    maintainers("cgmb", "srekolam", "renjithravindrankannath")
    libraries = ["libhipsolver"]

    version("develop", branch="develop")
    version("master", branch="master")

    version("5.4.3", sha256="02a1bffecc494393f49f97174db7d2c101db557d32404923a44520876e682e3a")
    version("5.4.0", sha256="d53d81c55b458ba5e6ea0ec6bd24bcc79ab06789730391da82d8c33b936339d9")
    version("5.3.3", sha256="f5a487a1c7225ab748996ac4d837ac7ab26b43618c4ed97a124f8fac1d67786e")
    version("5.3.0", sha256="6e920a59ddeefd52c9a6d164c33bc097726529e1ede3c417c711697956655b15")
    version("5.2.3", sha256="a57d883fdd09c6c7f9856fcfcabee6fa7ff9beed33d2f1a465bf28d38ea6f364")
    version("5.2.1", sha256="e000b08cf7bfb5f8f6d65d163ebeeb3274172b9f474228b810bde5e6f87f2b37")
    version("5.2.0", sha256="96927410e0a2cc0f50172604ef6437e15d2cf4b62d22b2035f13aae21f43dc82")
    version("5.1.3", sha256="96faa799a2db8078b72f9c3b5c199179875a7c20dc1064371b22a6a63397c145")
    version("5.1.0", sha256="697ba2b2814e7ac6f79680e6455b4b5e0def1bee2014b6940f47be7d13c0ae74")
    version(
        "5.0.2",
        sha256="cabeada451686ed7904a452c5f8fd3776721507db1c06f426cd8d7189ff4a441",
        deprecated=True,
    )
    version(
        "5.0.0",
        sha256="c59a5783dbbcb6a601c0e73d85d4a64d6d2c8f46009c01cb2b9886323f11e02b",
        deprecated=True,
    )
    version(
        "4.5.2",
        sha256="9807bf1da0da25940b546cf5d5d6064d46d837907e354e10c6eeb2ef7c296a93",
        deprecated=True,
    )
    version(
        "4.5.0",
        sha256="ee1176e977736a6e6fcba507fe6f56fcb3cefd6ba741cceb28464ea8bc476cd8",
        deprecated=True,
    )

    variant(
        "build_type",
        default="Release",
        values=("Release", "Debug", "RelWithDebInfo"),
        description="CMake build type",
    )

    depends_on("cmake@3.5:", type="build")

    depends_on("hip@4.1.0:", when="@4.1.0:")
    depends_on("rocm-cmake@master", type="build", when="@master:")
    depends_on("rocm-cmake@4.5.0:", type="build")

    for ver in ["master", "develop"]:
        depends_on("rocblas@" + ver, when="@" + ver)
        depends_on("rocsolver@" + ver, when="@" + ver)

    for ver in [
        "4.5.0",
        "4.5.2",
        "5.0.0",
        "5.0.2",
        "5.1.0",
        "5.1.3",
        "5.2.0",
        "5.2.1",
        "5.2.3",
        "5.3.0",
        "5.3.3",
        "5.4.0",
        "5.4.3",
    ]:
        depends_on("hip@" + ver, when="@" + ver)
        depends_on("rocblas@" + ver, when="@" + ver)
        depends_on("rocsolver@" + ver, when="@" + ver)

    depends_on("googletest@1.10.0:", type="test")
    depends_on("netlib-lapack@3.7.1:", type="test")

    def check(self):
        exe = join_path(self.build_directory, "clients", "staging", "hipsolver-test")
        self.run_test(exe, options=["--gtest_filter=-*known_bug*"])

    def setup_build_environment(self, env):
        env.set("CXX", self.spec["hip"].hipcc)

    @classmethod
    def determine_version(cls, lib):
        match = re.search(r"lib\S*\.so\.\d+\.\d+\.(\d)(\d\d)(\d\d)", lib)
        if match:
            ver = "{0}.{1}.{2}".format(
                int(match.group(1)), int(match.group(2)), int(match.group(3))
            )
        else:
            ver = None
        return ver

    def cmake_args(self):
        args = [
            self.define("BUILD_CLIENTS_SAMPLES", "OFF"),
            self.define("BUILD_CLIENTS_TESTS", self.run_tests),
        ]

        if self.spec.satisfies("@5.2.0:"):
            args.append(self.define("BUILD_FILE_REORG_BACKWARD_COMPATIBILITY", True))
        if self.spec.satisfies("@5.3.0:"):
            args.append(self.define("CMAKE_INSTALL_LIBDIR", "lib"))

        return args

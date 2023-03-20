# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Hipfort(CMakePackage):
    """Radeon Open Compute Parallel Primitives Library"""

    homepage = "https://github.com/ROCmSoftwarePlatform/hipfort"
    git = "https://github.com/ROCmSoftwarePlatform/hipfort.git"
    url = "https://github.com/ROCmSoftwarePlatform/hipfort/archive/rocm-5.4.3.tar.gz"
    tags = ["rocm"]

    maintainers("cgmb", "srekolam", "renjithravindrankannath")

    version("5.4.3", sha256="1954a1cba351d566872ced5549b2ced7ab6332221e2b98dba3c07180dce8f173")
    version("5.4.0", sha256="a781bc6d1dbb508a4bd6cc3df931696fac6c6361d4fd35efb12c9a04a72e112c")
    version("5.3.3", sha256="593be86502578b68215ffe767c26849fd27d4dbd92c8e76762275805f99e64f5")
    version("5.3.0", sha256="9e2aa142de45b2d2c29449d6f82293fb62844d511fbf51fa597845ba05c700fa")
    version("5.2.3", sha256="6648350ca4edc8757f0ae51d73a05a9a536808f19ad45f5b5ab84d420c72c9ec")
    version("5.2.1", sha256="ed53c9914d326124482751b81c4a353c6e64e87c1111124169a33513a3c49b42")
    version("5.2.0", sha256="a0af1fe62757993600a41af6bb6c4b8c6cfdfba650389645ac1f995f7623785c")
    version("5.1.3", sha256="8f8849d8d0972366bafa41be35cf6a7a59480ed584d1ddff39768cb14247e9d4")
    version("5.1.0", sha256="1ddd46c00bb6bcd539a921d6a94d858f4e4408a35cb6910186c7517f375ae8ab")
    version(
        "5.0.2",
        sha256="fcee6e62482ab15f365681dbc12bd9ae26b0fab2f2848a3c14de8ec63004a7aa",
        deprecated=True,
    )
    version(
        "5.0.0",
        sha256="af0f332fec082a03ca0403618ab20d31baadf3103e3371db9edc39dc9474ef4c",
        deprecated=True,
    )
    version(
        "4.5.2",
        sha256="14599d027b57189c6734b04ace7792d2ae5c409cf7983c0970b086fb4e634dd8",
        deprecated=True,
    )
    version(
        "4.5.0",
        sha256="48626dfb15bb5dcb044c9e1d4dc4b0654a2cd0abfc69485aa285dc20d7f40d51",
        deprecated=True,
    )
    version(
        "4.3.1",
        sha256="279a35edbc0c22fa930a4355e663a86adf4d0316c5b1b6b9ccc6ee5c19c8c2e4",
        deprecated=True,
    )
    version(
        "4.3.0",
        sha256="fd0ffdafdc17ac42c7dae3f89991651f15affdef9b2354da05c7493d09d8974e",
        deprecated=True,
    )
    version(
        "4.2.0",
        sha256="b411cb32bf87927eba4c5573b412c56d75d15165e2f1c8ac5ac18e624ed3a4b4",
        deprecated=True,
    )
    version(
        "4.1.0",
        sha256="2d335ae068d0cbb480575de7d3ea4868362af32cb195f911ee1aeced499f3974",
        deprecated=True,
    )
    version(
        "4.0.0",
        sha256="a497645c33e0eff39abd5344756de63424733cde2837b7376c924b44ed5ae9c9",
        deprecated=True,
    )
    version(
        "3.10.0",
        sha256="44173522d9eb2a18ec1cea2d9b00b237fe70501f0849bd6be3decbb73389487a",
        deprecated=True,
    )
    version(
        "3.9.0",
        sha256="a3c4e125a9b56820446a65bd76b8caa196fddb0e0723eb513f0bcde9abd6a0c0",
        deprecated=True,
    )
    version(
        "3.8.0",
        sha256="0132e9949f758dd8b8a462d133b3316101440cd503aa6c53bea9e34e61bbb3cc",
        deprecated=True,
    )

    variant(
        "build_type",
        default="Release",
        values=("Release", "Debug", "RelWithDebInfo"),
        description="CMake build type",
    )

    depends_on("cmake@3.0.2:", type="build")

    depends_on("rocm-cmake@3.8.0:", type="build")

    depends_on("binutils", when="%cce")

    for ver in [
        "3.8.0",
        "3.9.0",
        "3.10.0",
        "4.0.0",
        "4.1.0",
        "4.2.0",
        "4.3.0",
        "4.3.1",
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
        depends_on("hip@" + ver, type="build", when="@" + ver)

    def setup_build_environment(self, env):
        env.set("CXX", self.spec["hip"].hipcc)

    def cmake_args(self):
        args = []

        if self.spec.satisfies("^cmake@3.21.0:3.21.2"):
            args.append(self.define("__skip_rocmclang", "ON"))

        if self.spec.satisfies("%cce"):
            args.append("-DHIPFORT_COMPILER={}".format(spack_fc))
            args.append("-DHIPFORT_AR=" + join_path(self.spec["binutils"].prefix.bin, "ar"))
            args.append(
                "-DHIPFORT_RANLIB=" + join_path(self.spec["binutils"].prefix.bin, "ranlib")
            )
            args.append("-DHIPFORT_COMPILER_FLAGS='-ffree -eT'")

        return args

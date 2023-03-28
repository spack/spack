# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Hipfft(CMakePackage):
    """hipFFT is an FFT marshalling library. Currently, hipFFT supports
    either rocFFT or cuFFT as backends.hipFFT exports an interface that
    does not require the client to change, regardless of the chosen backend.
    It sits between the application and the backend FFT library, marshalling
    inputs into the backend and results back to the application."""

    homepage = "https://github.com/ROCmSoftwarePlatform/hipFFT"
    git = "https://github.com/ROCmSoftwarePlatform/hipFFT.git"
    url = "https://github.com/ROCmSoftwarePlatform/hipfft/archive/rocm-5.4.3.tar.gz"
    tags = ["rocm"]

    maintainers("renjithravindrankannath", "srekolam")

    version("master", branch="master")

    version("5.4.3", sha256="ae37f40b6019a11f10646ef193716836f366d269eab3c5cc2ed09af85355b945")
    version("5.4.0", sha256="d0a8e790182928b3d19774b8db1eece9b881a422f6a7055c051b12739fded624")
    version("5.3.3", sha256="fd1662cd5b1e1bce9db53b320c0fe614179cd196251efc2ef3365d38922b5cdc")
    version("5.3.0", sha256="ebbe2009b86b688809b6b4d5c3929fc589db455218d54a37790f21339147c5df")
    version("5.2.3", sha256="10be731fe91ede5e9f254f6eb3bc00b4dbeab449477f3cac03de358a7d0a6fa1")
    version("5.2.1", sha256="6c8fbace2864ca992b2fca9dc8d0bb4488aef62045acdfcf249d53dd005ebd35")
    version("5.2.0", sha256="ec37edcd61837281c403802ccc1cb01ec3fa3ba135b5ab16617961b66d4cc3e2")
    version("5.1.3", sha256="c26fa64499293b25d0686bed04feb61378c878a4bb4a6d559e6cb7be1f6bf2ec")
    version("5.1.0", sha256="1bac7761c055355216cd262cdc0450aabb383addcb739b56ba849b2e6e013fa5")
    version(
        "5.0.2",
        sha256="9ef64694f5def0d6fb98dc89e46d7a3f7d005a61348ac0b52184a3b8e84c2383",
        deprecated=True,
    )
    version(
        "5.0.0",
        sha256="867d0bdc6c9769c6cebc0c4594b24d5f3504157cdcef97a6a1668dd493ca6a15",
        deprecated=True,
    )
    version(
        "4.5.2",
        sha256="32ba6a5f50cfede3777a43794371ffb1363302131d8a0382d96df90ed7bc911a",
        deprecated=True,
    )
    version(
        "4.5.0",
        sha256="96636713bc6cdafbd5a9c1e98e816895448960c86b380fc0c3c9ffa28f670844",
        deprecated=True,
    )
    version(
        "4.3.1",
        sha256="429cfd40415856da8f5c2c321b612800d6826ee121df5a4e6d1596cad5b51727",
        deprecated=True,
    )
    version(
        "4.3.0",
        sha256="6e52e0eb5b2a13adaf317fe5b20b3e059589aabf2af87e4c67cb1022b861ba84",
        deprecated=True,
    )
    version(
        "4.2.0",
        sha256="74253b0d92feff55ebb39b3fe4a22a6454160a60bdad37384aa5340fd8843f8a",
        deprecated=True,
    )
    version(
        "4.1.0",
        sha256="885ffd4813f2c271150f1b8b386f0af775b38fc82b96ce6fd94eb4ba0c0180be",
        deprecated=True,
    )

    variant(
        "build_type",
        default="Release",
        values=("Release", "Debug", "RelWithDebInfo"),
        description="CMake build type",
    )

    depends_on("cmake@3.5:", type="build")

    for ver in [
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
        depends_on("rocm-cmake@%s:" % ver, type="build", when="@" + ver)
        depends_on("hip@" + ver, when="@" + ver)
        depends_on("rocfft@" + ver, when="@" + ver)

    def setup_build_environment(self, env):
        env.set("CXX", self.spec["hip"].hipcc)

    def cmake_args(self):
        args = [
            # Make sure find_package(HIP) finds the module.
            self.define("BUILD_CLIENTS_SAMPLES", "OFF")
        ]

        if self.spec.satisfies("^cmake@3.21.0:3.21.2"):
            args.append(self.define("__skip_rocmclang", "ON"))

        if self.spec.satisfies("@3.7.0:5.1"):
            args.append(self.define("CMAKE_MODULE_PATH", self.spec["hip"].prefix.cmake))
        elif self.spec.satisfies("@5.2.0:"):
            args.append(self.define("CMAKE_MODULE_PATH", self.spec["hip"].prefix.lib.cmake.hip))
            args.append(self.define("BUILD_FILE_REORG_BACKWARD_COMPATIBILITY", True))

        if self.spec.satisfies("@5.3.0:"):
            args.append(self.define("CMAKE_INSTALL_LIBDIR", "lib"))
        return args

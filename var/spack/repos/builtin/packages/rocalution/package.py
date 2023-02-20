# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import itertools

from spack.package import *


class Rocalution(CMakePackage):
    """rocALUTION is a sparse linear algebra library with focus on
    exploring fine-grained parallelism on top of AMD's Radeon Open
    eCosystem Platform ROCm runtime and toolchains, targeting modern
    CPU and GPU platforms. Based on C++ and HIP, it provides a portable,
     generic and flexible design that allows seamless integration with
    other scientific software packages."""

    homepage = "https://github.com/ROCmSoftwarePlatform/rocALUTION"
    git = "https://github.com/ROCmSoftwarePlatform/rocALUTION.git"
    url = "https://github.com/ROCmSoftwarePlatform/rocALUTION/archive/rocm-5.4.3.tar.gz"
    tags = ["rocm"]

    maintainers("cgmb", "srekolam", "renjithravindrankannath")
    libraries = ["librocalution_hip"]

    version("5.4.3", sha256="39d00951a9b3cbdc4205a7e3ce75c026d9428c71c784815288c445f84a7f8a0e")
    version("5.4.0", sha256="dccf004434e0fee6d0c7bedd46827f5a2af0392bc4807a08403b130e461f55eb")
    version("5.3.3", sha256="3af022250bc25bebdee12bfb8fdbab4b60513b537b9fe15dfa82ded8850c5066")
    version("5.3.0", sha256="f623449789a5c9c9137ae51d4dbbee5c6940d8813826629cb4b7e84f07fab494")
    version("5.2.3", sha256="8e0d77099bf7dc0d00505e1c936b072a59719102c75398dc1416cbef31902253")
    version("5.2.1", sha256="f246bd5b5d1b5821c29b566610a1c1d5c5cc361e0e5c373b8b04168b05e9b26f")
    version("5.2.0", sha256="a5aac471bbec87d019ad7c6db779c73327ad40ecdea09dc5ab2106e62cd6b7eb")
    version("5.1.3", sha256="7febe8179f120cbe58ea255bc233ad5d1b4c106f3934eb8e670135a8b7bd09c7")
    version("5.1.0", sha256="d9122189103ebafe7ec5aeb50e60f3e02af5c2747021f9071aab91e7f875c29e")
    version(
        "5.0.2",
        sha256="b01adaf858b9c3683523b087a55fafb655864f5db8e2a1acdbf588f53d6972e2",
        deprecated=True,
    )
    version(
        "5.0.0",
        sha256="df9e7eacb8cc1bd5c7c4071b20356a885ee8ae13e6ab5afdabf88a272ab32c7e",
        deprecated=True,
    )
    version(
        "4.5.2",
        sha256="8be38922320cd9d4fc465a30f0322843849f62c0c7dad2bdbe52290a1b69d2a0",
        deprecated=True,
    )
    version(
        "4.5.0",
        sha256="191629fef002fd1a0793a6b4fe5a6b8c43ac49d3cd173ba64a91359f54659e5b",
        deprecated=True,
    )
    version(
        "4.3.1",
        sha256="d3a7b9290f99bdc7382d1d5259c3f5e0e66a43aef4d05b7c2cd78b0e4a5c59bc",
        deprecated=True,
    )
    version(
        "4.3.0",
        sha256="f064b96f9f04cf22b89f95f72147fcfef28e2c56ecd764008c060f869c74c144",
        deprecated=True,
    )
    version(
        "4.2.0",
        sha256="0424adf522ded41de5b77666e04464a25c73c92e34025762f30837f90a797445",
        deprecated=True,
    )
    version(
        "4.1.0",
        sha256="3f61be18a02dff0c152a0ad7eb4779c43dd744b0ba172aa6a4267fc596d582e4",
        deprecated=True,
    )
    version(
        "4.0.0",
        sha256="80a224a5c19dea290e6edc0e170c3dff2e726c2b3105d599ec6858cc66f076a9",
        deprecated=True,
    )
    version(
        "3.10.0",
        sha256="c24cb9d1a8a1a3118040b8b16dec7c06268bcf157424d3378256cc9eb93f1b58",
        deprecated=True,
    )
    version(
        "3.9.0",
        sha256="1ce36801fe1d44f743b46b43345c0cd90d76b73911b2ec97be763f93a35396fb",
        deprecated=True,
    )
    version(
        "3.8.0",
        sha256="39e64a29e75c4276163a93596436064c6338770ca72ce7f43711ed8285ed2de5",
        deprecated=True,
    )
    version(
        "3.7.0",
        sha256="4d6b20aaaac3bafb7ec084d684417bf578349203b0f9f54168f669e3ec5699f8",
        deprecated=True,
    )
    version(
        "3.5.0",
        sha256="be2f78c10c100d7fd9df5dd2403a44700219c2cbabaacf2ea50a6e2241df7bfe",
        deprecated=True,
    )

    amdgpu_targets = ROCmPackage.amdgpu_targets

    variant("amdgpu_target", values=auto_or_any_combination_of(*amdgpu_targets), sticky=True)
    variant(
        "build_type",
        default="Release",
        values=("Release", "Debug", "RelWithDebInfo"),
        description="CMake build type",
    )

    depends_on("cmake@3.5:", type="build")
    for ver in ["3.5.0", "3.7.0", "3.8.0"]:
        depends_on("hip@" + ver, when="@" + ver)
        depends_on("rocprim@" + ver, when="@" + ver)
        for tgt in itertools.chain(["auto"], amdgpu_targets):
            rocblas_tgt = tgt if tgt != "gfx900:xnack-" else "gfx900"
            depends_on(
                "rocblas@{0} amdgpu_target={1}".format(ver, rocblas_tgt),
                when="@{0} amdgpu_target={1}".format(ver, tgt),
            )
            depends_on(
                "rocsparse@{0} amdgpu_target={1}".format(ver, tgt),
                when="@{0} amdgpu_target={1}".format(ver, tgt),
            )
        depends_on("rocm-cmake@%s:" % ver, type="build", when="@" + ver)

    for ver in [
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
        depends_on("hip@" + ver, when="@" + ver)
        depends_on("rocprim@" + ver, when="@" + ver)
        for tgt in itertools.chain(["auto"], amdgpu_targets):
            rocblas_tgt = tgt if tgt != "gfx900:xnack-" else "gfx900"
            depends_on(
                "rocblas@{0} amdgpu_target={1}".format(ver, rocblas_tgt),
                when="@{0} amdgpu_target={1}".format(ver, tgt),
            )
            depends_on(
                "rocsparse@{0} amdgpu_target={1}".format(ver, tgt),
                when="@{0} amdgpu_target={1}".format(ver, tgt),
            )
            depends_on(
                "rocrand@{0} amdgpu_target={1}".format(ver, tgt),
                when="@{0} amdgpu_target={1}".format(ver, tgt),
            )
        depends_on("rocm-cmake@%s:" % ver, type="build", when="@" + ver)

    depends_on("googletest@1.10.0:", type="test")
    # This fix is added to address the compilation failure and it is
    # already taken in 5.2.3 rocm release.
    patch("0003-fix-compilation-for-rocalution-5.2.0.patch", when="@5.2")
    # Fix build for most Radeon 5000 and Radeon 6000 series GPUs.
    patch("0004-fix-navi-1x.patch", when="@5.2.0:5.3")

    def check(self):
        exe = join_path(self.build_directory, "clients", "staging", "rocalution-test")
        self.run_test(exe)

    def setup_build_environment(self, env):
        env.set("CXX", self.spec["hip"].hipcc)

    def patch(self):
        if "@3.9.0:" in self.spec:
            kwargs = {"ignore_absent": False, "backup": False, "string": False}

            with working_dir("src/base/hip"):
                match = "^#include <rocrand/rocrand.hpp>"
                substitute = "#include <rocrand.hpp>"
                files = ["hip_rand_normal.hpp", "hip_rand_uniform.hpp"]
                filter_file(match, substitute, *files, **kwargs)

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
            self.define("SUPPORT_HIP", "ON"),
            self.define("SUPPORT_MPI", "OFF"),
            self.define("BUILD_CLIENTS_SAMPLES", "OFF"),
            self.define("BUILD_CLIENTS_TESTS", self.run_tests),
        ]
        if self.spec.satisfies("@3.7.0:5.1.3"):
            args.append(self.define("CMAKE_MODULE_PATH", self.spec["hip"].prefix.cmake))
        elif self.spec.satisfies("@5.2.0:"):
            args.append(self.define("CMAKE_MODULE_PATH", self.spec["hip"].prefix.lib.cmake.hip))
        if "auto" not in self.spec.variants["amdgpu_target"]:
            args.append(self.define_from_variant("AMDGPU_TARGETS", "amdgpu_target"))

        if self.spec.satisfies("^cmake@3.21.0:3.21.2"):
            args.append(self.define("__skip_rocmclang", "ON"))

        if self.spec.satisfies("@5.2.0:"):
            args.append(self.define("BUILD_FILE_REORG_BACKWARD_COMPATIBILITY", True))

        if self.spec.satisfies("@5.3.0:"):
            args.append("-DCMAKE_INSTALL_LIBDIR=lib")

        return args

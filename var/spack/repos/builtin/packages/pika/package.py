# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import sys

from spack.package import *


class Pika(CMakePackage, CudaPackage, ROCmPackage):
    """C++ runtime system for parallellism and concurrency."""

    homepage = "https://github.com/pika-org/pika/"
    url = "https://github.com/pika-org/pika/archive/0.0.0.tar.gz"
    git = "https://github.com/pika-org/pika.git"
    maintainers("msimberg", "albestro", "teonnik", "aurianer")

    version("0.13.0", sha256="67e0843141fb711787e71171a7a669c9cdb9587e4afd851ee2b0339a62b9a254")
    version("0.12.0", sha256="daa1422eb73d6a897ce7b8ff8022e09e7b0fec83d92728ed941a92e57dec5da3")
    version("0.11.0", sha256="3c3d94ca1a3960884bad7272bb9434d61723f4047ebdb097fcf522c6301c3fda")
    version("0.10.0", sha256="3b443b8f0f75b9a558accbaef0334a113a71b0205770e6c7ff02ea2d7c6aca5b")
    version("0.9.0", sha256="c349b2a96476d6974d2421288ca4d2e14ef9e5897d44cd7d5343165faa2d1299")
    version("0.8.0", sha256="058e82d7c8f95badabe52bbb4682d55aadf340d67ced1226c0673b4529adc182")
    version("0.7.0", sha256="e1bf978c88515f7af28ee47f98b795ffee521c15b39877ea4cfb405f31d507ed")
    version("0.6.0", sha256="cb4ebd7b92da39ec4df7b0d05923b94299d6ee2f2f49752923ffa2266ca76568")
    version("0.5.0", sha256="c43de7e92d04bea0ce59716756ef5f3a5a54f9e4affed872c1468632ad855f7c")
    version("0.4.0", sha256="31084a0a61103ee9574aaa427f879682e3e37cb11e8d147f2649949bee324591")
    version("0.3.0", sha256="bbb89f9824c58154ed59e2e14276c0ad132fd7b90b2be64ddd0e284f3b57cc0f")
    version("0.2.0", sha256="712bb519f22bdc9d5ee4ac374d251a54a0af4c9e4e7f62760b8ab9a177613d12")
    version("0.1.0", sha256="aa0ae2396cd264d821a73c4c7ecb118729bb3de042920c9248909d33755e7327")
    version("main", branch="main")

    generator = "Ninja"

    map_cxxstd = lambda cxxstd: "2a" if cxxstd == "20" else cxxstd
    cxxstds = ("17", "20")
    variant(
        "cxxstd",
        default="17",
        values=cxxstds,
        description="Use the specified C++ standard when building",
    )

    variant(
        "malloc",
        default="mimalloc",
        description="Define which allocator will be linked in",
        values=("system", "jemalloc", "mimalloc", "tbbmalloc", "tcmalloc"),
    )

    default_generic_coroutines = True
    if sys.platform.startswith("linux") or sys.platform == "win32":
        default_generic_coroutines = False
    variant(
        "generic_coroutines",
        default=default_generic_coroutines,
        description="Use Boost.Context as the underlying coroutines"
        " context switch implementation",
    )

    variant("examples", default=False, description="Build and install examples")
    variant("mpi", default=False, description="Enable MPI support")
    variant("apex", default=False, description="Enable APEX support", when="@0.2:")
    variant("tracy", default=False, description="Enable Tracy support", when="@0.7:")
    variant(
        "p2300",
        default=False,
        description="Use P2300 reference implementation for sender/receiver functionality",
        when="@0.9:",
    )

    # Build dependencies
    depends_on("git", type="build")
    depends_on("ninja", type="build")
    depends_on("cmake@3.18:", type="build")
    depends_on("cmake@3.22:", when="@0.8:", type="build")

    conflicts("%gcc@:6")
    conflicts("%clang@:6")
    # Pika is requiring the std::filesystem support starting from version 0.2.0
    conflicts("%gcc@:8", when="@0.2:")
    conflicts("%clang@:8", when="@0.2:")
    conflicts("+p2300", when="cxxstd=17")

    # Other dependencies
    depends_on("boost@1.71:")
    depends_on("fmt@9:", when="@0.11:")
    depends_on("hwloc@1.11.5:")

    depends_on("gperftools", when="malloc=tcmalloc")
    depends_on("jemalloc", when="malloc=jemalloc")
    depends_on("mimalloc", when="malloc=mimalloc")
    depends_on("tbb", when="malloc=tbbmalloc")

    depends_on("apex", when="+apex")
    depends_on("cuda@11:", when="+cuda")
    depends_on("hip@5.2:", when="@0.8: +rocm")
    depends_on("hipblas", when="@:0.8 +rocm")
    depends_on("mpi", when="+mpi")
    depends_on("stdexec", when="+p2300")
    depends_on("rocblas", when="+rocm")
    depends_on("rocsolver", when="@0.5: +rocm")
    depends_on("tracy-client", when="+tracy")
    conflicts("tracy-client@0.9:", when="@:0.9")
    depends_on("whip@0.1: +rocm", when="@0.9: +rocm")
    depends_on("whip@0.1: +cuda", when="@0.9: +cuda")

    with when("+rocm"):
        for val in ROCmPackage.amdgpu_targets:
            depends_on(
                "whip@0.1: amdgpu_target={0}".format(val),
                when="@0.9: amdgpu_target={0}".format(val),
            )
            depends_on(
                "rocsolver amdgpu_target={0}".format(val),
                when="@0.5: amdgpu_target={0}".format(val),
            )
            depends_on(
                "rocblas amdgpu_target={0}".format(val), when="amdgpu_target={0}".format(val)
            )

    with when("+cuda"):
        for val in CudaPackage.cuda_arch_values:
            depends_on(
                "whip@0.1: cuda_arch={0}".format(val), when="@0.9: cuda_arch={0}".format(val)
            )

    for cxxstd in cxxstds:
        depends_on("boost cxxstd={0}".format(map_cxxstd(cxxstd)), when="cxxstd={0}".format(cxxstd))
        depends_on("fmt cxxstd={0}".format(cxxstd), when="@0.11: cxxstd={0}".format(cxxstd))

    # COROUTINES
    # ~generic_coroutines conflict is not fully implemented
    # for additional information see:
    # https://github.com/spack/spack/pull/17654
    # https://github.com/STEllAR-GROUP/hpx/issues/4829
    depends_on("boost+context", when="+generic_coroutines")
    depends_on("boost+atomic+chrono+thread", when="@:0.3.0+generic_coroutines")
    _msg_generic_coroutines = "This platform requires +generic_coroutines"
    conflicts("~generic_coroutines", when="platform=darwin", msg=_msg_generic_coroutines)

    # Patches
    patch("transform_mpi_includes.patch", when="@0.3.0 +mpi")
    patch("mimalloc_no_version_requirement.patch", when="@:0.5 malloc=mimalloc")

    # Fix missing template instantiation on macOS
    patch(
        "https://github.com/pika-org/pika/commit/dd1dfb85781ec2e76fa37ce7311323e69fbe42a1.patch?full_index=1",
        sha256="2944f746f5ae4385aba11b7c4a2f991abc108b08ea3dc394bf61c20fc7a2c4f2",
        when="@0.7.0 platform=darwin",
    )

    # Fix constexpr/fmt bug on macOS
    # Upstream patch is
    # https://github.com/pika-org/pika/commit/33655188fe4b9bcfad1e98a05e9ebcc22afc7ef8.patch,
    # but it requires changes to apply to 0.11.0.
    patch("thread_id_fmt.patch", when="@0.11 platform=darwin")

    def cmake_args(self):
        spec, args = self.spec, []

        args += [
            self.define("PIKA_WITH_CXX_STANDARD", spec.variants["cxxstd"].value),
            self.define_from_variant("PIKA_WITH_EXAMPLES", "examples"),
            self.define_from_variant("PIKA_WITH_MALLOC", "malloc"),
            self.define_from_variant("PIKA_WITH_CUDA", "cuda"),
            self.define_from_variant("PIKA_WITH_HIP", "rocm"),
            self.define_from_variant("PIKA_WITH_MPI", "mpi"),
            self.define_from_variant("PIKA_WITH_APEX", "apex"),
            self.define_from_variant("PIKA_WITH_TRACY", "tracy"),
            self.define("PIKA_WITH_TESTS", self.run_tests),
            self.define_from_variant("PIKA_WITH_GENERIC_CONTEXT_COROUTINES", "generic_coroutines"),
            self.define_from_variant("PIKA_WITH_P2300_REFERENCE_IMPLEMENTATION", "p2300"),
            self.define("BOOST_ROOT", spec["boost"].prefix),
            self.define("HWLOC_ROOT", spec["hwloc"].prefix),
        ]

        # HIP support requires compiling with hipcc for < 0.8.0
        if self.spec.satisfies("@:0.7 +rocm"):
            args += [self.define("CMAKE_CXX_COMPILER", self.spec["hip"].hipcc)]
            if self.spec.satisfies("^cmake@3.21.0:3.21.2"):
                args += [self.define("__skip_rocmclang", True)]
        if self.spec.satisfies("@0.8: +rocm"):
            rocm_archs = spec.variants["amdgpu_target"].value
            if "none" not in rocm_archs:
                rocm_archs = ";".join(rocm_archs)
                args.append(self.define("CMAKE_HIP_ARCHITECTURES", rocm_archs))

        return args

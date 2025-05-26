# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack_repo.builtin.build_systems.cmake import CMakePackage

from spack.package import *


class RocmExamples(CMakePackage):
    """A collection of examples for the ROCm software stack"""

    homepage = "https://github.com/ROCm/rocm-examples"
    url = "https://github.com/ROCm/rocm-examples/archive/refs/tags/rocm-6.2.1.tar.gz"

    tags = ["rocm"]

    maintainers("srekolam", "renjithravindrankannath", "afzpatel")

    license("MIT")

    version("6.4.0", sha256="af2be5806982a72c726cf052c512493cc004bfa98d0136fbf8fed2754a4f4b80")
    version("6.3.3", sha256="5e5bdffb4bf56d30c5f8dd8fda95d162362d17e446396e6b6a3afe8d293039f3")
    version("6.3.2", sha256="7a71dcfec782338af1d838f86b692974368e362de8ad85d5ec26c23b0afbab9e")
    version("6.3.1", sha256="c5093cd6641de478b940d2e36d6723f7ef1ccad3f4f96caf0394def2e6c7e325")
    version("6.3.0", sha256="809b5212d86d182586d676752b192967aee3bde6df8bbbe67558b221d63f5c7c")
    version("6.2.4", sha256="510931103e4a40b272123b5c731d2ea795215c6171810beb1d5335d73bcc9b03")
    version("6.2.1", sha256="2e426572aa5f5b44c7893ea256945c8733b79db39cca84754380f40c8b44a563")
    version("6.2.0", sha256="6fb1f954ed32b5c4085c7f071058d278c2e1e8b7b71118ee5e85cf9bbc024df0")

    variant("rocm", default=True, description="Build with ROCm")
    variant("cuda", default=False, description="Build with CUDA")

    conflicts("+cuda +rocm", msg="CUDA and ROCm support are mutually exclusive")
    conflicts("~cuda ~rocm", msg="CUDA or ROCm support is required")

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    depends_on("glfw", type="build")

    for ver in ["6.4.0", "6.3.3", "6.3.2", "6.3.1", "6.3.0", "6.2.4", "6.2.1", "6.2.0"]:
        depends_on(f"hip@{ver}", when=f"@{ver}")
        depends_on(f"hipify-clang@{ver}", when=f"@{ver}")
        depends_on(f"hipcub@{ver}", when=f"@{ver}")
        depends_on(f"hipsolver@{ver}", when=f"@{ver}")
        depends_on(f"hipblas@{ver}", when=f"@{ver}")
        depends_on(f"hiprand@{ver}", when=f"@{ver} +rocm")
        depends_on(f"rocblas@{ver}", when=f"@{ver} +rocm")
        depends_on(f"rocthrust@{ver}", when=f"@{ver} +rocm")
        depends_on(f"rocsparse@{ver}", when=f"@{ver} +rocm")
        depends_on(f"rocsolver@{ver}", when=f"@{ver} +rocm")

    for ver in ["6.4.0", "6.3.3", "6.3.2", "6.3.1", "6.3.0"]:
        depends_on(f"hipfft@{ver}", when=f"@{ver}")
        depends_on(f"rocfft@{ver}", when=f"@{ver} +rocm")

    depends_on("hip+cuda", when="+cuda")
    depends_on("hipcub+cuda", when="+cuda")
    depends_on("hipsolver+cuda", when="+cuda")
    depends_on("hipblas+cuda", when="+cuda")
    depends_on("hipfft+cuda", when="@6.3: +cuda")

    patch(
        "https://github.com/ROCm/rocm-examples/commit/669fc3e90ce95567464e80d7925f45cb525c81db.patch?full_index=1",
        sha256="ee0eec2140732513d077cca2a46a8257ed785315208dd3e917e4c8e424cfa63e",
        when="@6.4+cuda",
    )
    patch("add_hip_include_cuda.patch", when="@6.4+cuda")

    def patch(self):
        filter_file(
            r"${ROCM_ROOT}/bin/hipify-perl",
            f"{self.spec['hipify-clang'].prefix}/bin/hipify-perl",
            "HIP-Basic/hipify/CMakeLists.txt",
            string=True,
        )

    def cmake_args(self):
        args = []
        if self.spec.satisfies("+cuda"):
            args.append(
                self.define(
                    "OFFLOAD_BUNDLER_COMMAND",
                    f"{self.spec['llvm-amdgpu'].prefix}/bin/clang-offload-bundler",
                )
            )
            args.append(
                self.define("LLVM_MC_COMMAND", f"{self.spec['llvm-amdgpu'].prefix}/bin/llvm-mc")
            )
            args.append(
                self.define("LLVM_DIS_COMMAND", f"{self.spec['llvm-amdgpu'].prefix}/bin/llvm-dis")
            )
        if self.spec.satisfies("+cuda"):
            args.append(self.define("GPU_RUNTIME", "CUDA"))
            args.append(self.define("CMAKE_MODULE_PATH", self.spec["hip"].prefix.lib.cmake.hip))
            args.append(self.define("ROCM_ROOT", self.spec["hip"].prefix))
            args.append(self.define("HIP_ROOT_DIR", self.spec["hip"].prefix))
            args.append(
                self.define(
                    "CUDA_DRIVER_LIB",
                    f"{self.spec['cuda'].prefix}/targets/x86_64-linux/lib/stubs/libcuda.so",
                )
            )
            # TODO: enable reduction for +cuda
            args.append(self.define("REDUCTION_BUILD_EXAMPLES", False))
            args.append(self.define("REDUCTION_BUILD_TESTING", False))
            args.append(self.define("REDUCTION_BUILD_BENCHMARKS", False))
        return args

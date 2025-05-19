# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack_repo.builtin.build_systems.cmake import CMakePackage

from spack.package import *


class Rocjpeg(CMakePackage):
    """rocJPEG is a high-performance jpeg decode SDK for decoding jpeg images
    using a hardware-accelerated jpeg decoder on AMD's GPUs."""

    homepage = "https://github.com/ROCm/rocJPEG"
    git = "https://github.com/ROCm/rocJPEG.git"
    url = "https://github.com/ROCm/rocJPEG/archive/refs/tags/rocm-6.3.0.tar.gz"

    maintainers("afzpatel", "srekolam", "renjithravindrankannath")

    license("MIT")

    version("6.4.0", sha256="5488f5ab9c475566716d99ad32fb4c20686ac1bcc00c9242221abdbde2b94ffe")
    version("6.3.3", sha256="65081b20ab3df82337fdcaf3d4e614c75f946656a4ea7bc00ac0d1bbd81e3e83")
    version("6.3.2", sha256="4e1ec9604152e818afa85360f1e0ef9e98bfb8a97ca0989980063e2ece015c16")
    version("6.3.1", sha256="f4913cbc63e11b9b418d33b0f9ba0fec0aa00b23285090acfd435e1ba1c21e42")
    version("6.3.0", sha256="2623b8f8bb61cb418d00c695e8ff0bc5979e1bb2d61d6c327a27d676c89e89cb")

    depends_on("cxx", type="build")

    for ver in ["6.3.0", "6.3.1", "6.3.2", "6.3.3", "6.4.0"]:
        depends_on(f"llvm-amdgpu@{ver}", when=f"@{ver}")
        depends_on(f"hip@{ver}", when=f"@{ver}")

    depends_on("libva", type="build", when="@6.2:")
    depends_on("libdrm", type="build", when="@6.4:")
    patch("0001-add-amdgpu-drm-include.patch", when="@6.4")

    def patch(self):
        filter_file(
            r"${ROCM_PATH}/lib/llvm/bin/clang++",
            "{0}/bin/clang++".format(self.spec["llvm-amdgpu"].prefix),
            "CMakeLists.txt",
            string=True,
        )

    def cmake_args(self):
        args = [self.define("LIBVA_INCLUDE_DIR", self.spec["libva"].prefix.include)]
        if self.spec.satisfies("@6.4.0:"):
            args.append(
                self.define("CMAKE_C_COMPILER", f"{self.spec['llvm-amdgpu'].prefix}/bin/amdclang")
            )
            args.append(
                self.define(
                    "CMAKE_CXX_COMPILER", f"{self.spec['llvm-amdgpu'].prefix}/bin/amdclang++"
                )
            )
            args.append(self.define("AMDGPU_DRM_INCLUDE_DIRS", self.spec["libdrm"].prefix.include))
        return args

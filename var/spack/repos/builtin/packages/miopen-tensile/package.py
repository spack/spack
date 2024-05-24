# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re

from spack.package import *


class MiopenTensile(CMakePackage):
    """MIOpenTensile provides host-callable interfaces to Tensile library.
    MIOpenTensile supports one programming model: HIP"""

    homepage = "https://github.com/ROCm/MIOpenTensile"
    git = "https://github.com/ROCm/MIOpenTensile.git"
    url = "https://github.com/ROCm/MIOpentensile/archive/rocm-5.0.0.tar.gz"
    tags = ["rocm"]

    maintainers("srekolam")
    libraries = ["libMIOpenTensile"]

    version("5.1.0", sha256="f1ae57bd4df8c154357b3f17caf0cfd5f80ba16ffff67bf6219a56f1eb5f897d")

    tensile_architecture = ("all", "gfx906", "gfx908", "gfx803", "gfx900")

    variant(
        "tensile_architecture",
        default="all",
        description="AMD GPU architecture",
        values=tensile_architecture,
        multi=True,
    )
    variant(
        "build_type",
        default="Release",
        values=("Release", "Debug", "RelWithDebInfo"),
        description="CMake build type",
    )

    patch("0002-Improve-compilation-by-using-local-tensile-path.patch", when="@4.5.0:")

    depends_on("cmake@3.5:", type="build")
    depends_on("msgpack-c@3:")
    depends_on("python@3.6:", type="build")
    depends_on("py-virtualenv", type="build")
    depends_on("perl-file-which", type="build")
    depends_on("py-pyyaml", type="build")
    depends_on("py-wheel", type="build")
    depends_on("py-msgpack", type="build")
    depends_on("py-pip", type="build")

    resource(
        name="Tensile",
        git="https://github.com/ROCm/Tensile.git",
        commit="9cbabb07f81e932b9c98bf5ae48fbd7fcef615cf",
    )

    for ver in ["5.1.0"]:
        depends_on(f"rocm-cmake@{ver}:", type="build", when=f"@{ver}")
        depends_on(f"hip@{ver}", when=f"@{ver}")
        depends_on(f"llvm-amdgpu@{ver}", when=f"@{ver}")
        depends_on(f"rocminfo@{ver}", when=f"@{ver}")

    def setup_build_environment(self, env):
        env.set("CXX", self.spec["hip"].hipcc)

    @classmethod
    def determine_version(cls, lib):
        match = re.search(r"lib\S*\.so\.\d+\.\d+\.(\d)(\d\d)(\d\d)", lib)
        if match:
            return "{0}.{1}.{2}".format(
                int(match.group(1)), int(match.group(2)), int(match.group(3))
            )
        return None

    def cmake_args(self):
        arch = self.spec.variants["tensile_architecture"].value
        tensile_path = join_path(self.stage.source_path, "Tensile")
        args = [
            self.define("TENSILE_USE_MSGPACK", "ON"),
            self.define("COMPILER", "hipcc"),
            self.define("TENSILE_USE_LLVM", "OFF"),
            self.define("CODE_OBJECT_VERSION", "V3"),
            self.define("TENSILE_LIBRARY_FORMAT", "msgpack"),
            self.define("MIOPEN_TENSILE_SRC", "asm_full"),
            self.define("Tensile_TEST_LOCAL_PATH", tensile_path),
        ]
        args.append(self.define("Tensile_ARCHITECTURE", arch))

        return args

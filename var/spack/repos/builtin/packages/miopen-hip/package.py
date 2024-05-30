# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re

from spack.package import *
from spack.pkg.builtin.boost import Boost


class MiopenHip(CMakePackage):
    """AMD's library for high performance machine learning primitives."""

    homepage = "https://github.com/ROCm/MIOpen"
    git = "https://github.com/ROCm/MIOpen.git"
    url = "https://github.com/ROCm/MIOpen/archive/rocm-6.1.1.tar.gz"
    tags = ["rocm"]

    maintainers("srekolam", "renjithravindrankannath")
    libraries = ["libMIOpen"]

    license("MIT")
    version("6.1.1", sha256="cf568ea16dd23b32fe89e250bb33ed4722fea8aa7f407cc66ff37c37aab037ce")
    version("6.1.0", sha256="3b373117eaeaf618aab9b39bb22e9950fd49bd0e264c8587b0c51fa348afe0d1")
    version("6.0.2", sha256="e6f671bd6af59f7470f42cda2ff9e77441d8f6c2105772bbf855d31da1085ffa")
    version("6.0.0", sha256="a0718a48353be30ff98118ade511f0c1b454e394d8f934aefe7dd6946562b2e9")
    version("5.7.1", sha256="912a658fe21ce6f1982b0f2ff251c3f7bb618f2e7e9876d983bcb54e3cd7129e")
    version("5.7.0", sha256="5cd0b62254469e1c246d5890d2b78f8aedcf42cf8a327eabc1a391b83bcd14e1")
    version("5.6.1", sha256="ff627d68ed9e52433a3c808b5d3ff179a398b77ce81b00cfea7b2c4da5162c6c")
    version("5.6.0", sha256="d620ddab5b488bdf81242654fefa337c6b71dc410c2ff26d30a4ee86a8d22d11")
    version("5.5.1", sha256="2cd75071b8ee876c69a94f028b6c8a9346d6d2fde7d4b64e6d635f3b6c994262")
    version("5.5.0", sha256="791087242551669e546225e36123c21663f0dad14dbcfd6d0ce0e7bad0ab0de1")
    version("5.4.3", sha256="37ffe2ed3d7942da8ea2f6bdb85c7a2f58e3ccd31767db158a322769d3604efd")
    version("5.4.0", sha256="b4153791f9eeee4cbc5534bc6ad8b32c0947bcd38e08b77ebe144065a4fa5456")
    version("5.3.3", sha256="7efc98215d23a2caaf212378c37e9a6484f54a4ed3e9660719286e4f287d3715")
    version("5.3.0", sha256="c5819f593d71beeda2eb24b89182912240cc40f83b2b8f9de695a8e230aa4ea6")
    with default_args(deprecated=True):
        version("5.2.3", sha256="28747847446955b3bab24f7fc65c1a6b863a12f12ad3a35e0312072482d38122")
        version("5.2.1", sha256="0977a8876d41bbd2fa268341c93892f35878d7efc1711194ad87582f877ff500")
        version("5.2.0", sha256="5fda69426e81df9f8fb6658e579176b9c4fcce3516fc8488d3cfd2b6f6f2b3b4")
        version("5.1.3", sha256="510461f5c5bdbcf8dc889099d1e5960b9f84bd845a9fc9154588a9898c701c1d")
        version("5.1.0", sha256="bb50201334d68addf153b84b88ab803027c4913d71bdbda6f5ccde3f672f6fdd")

    depends_on("cmake@3.5:", type="build")
    depends_on("pkgconfig", type="build")

    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on('boost +filesystem')
    # See https://github.com/spack/spack/pull/22303 for reference
    depends_on(Boost.with_default_variants)
    depends_on("boost@1.67.0:1.73.0")
    depends_on("bzip2")
    depends_on("sqlite")
    depends_on("half")
    depends_on("zlib-api")

    patch("miopen-hip-include-nlohmann-include-directory.patch", when="@5.4.0:5.7")
    patch("0002-add-include-dir-miopen-hip-6.0.0.patch", when="@6.0")
    patch("0002-add-include-dir-miopen-hip-6.1.0.patch", when="@6.1")
    patch(
        "https://github.com/ROCm/MIOpen/commit/f60aa1ff89f8fb596b4a6a4c70aa7d557803db87.patch?full_index=1",
        sha256="7f382c872d89f22da1ad499e85ffe9881cc7404c8465e42877a210a09382e2ea",
        when="@5.7",
    )

    for ver in [
        "5.1.0",
        "5.1.3",
        "5.2.0",
        "5.2.1",
        "5.2.3",
        "5.3.0",
        "5.3.3",
        "5.4.0",
        "5.4.3",
        "5.5.0",
        "5.5.1",
        "5.6.0",
        "5.6.1",
        "5.7.0",
        "5.7.1",
        "6.0.0",
        "6.0.2",
        "6.1.0",
        "6.1.1",
    ]:
        depends_on(f"rocm-cmake@{ver}:", type="build", when=f"@{ver}")
        depends_on(f"hip@{ver}", when=f"@{ver}")
        depends_on(f"rocm-clang-ocl@{ver}", when=f"@{ver}")
        depends_on(f"rocblas@{ver}", when=f"@{ver}")

    for ver in ["5.1.0", "5.1.3", "5.2.0", "5.2.1", "5.2.3", "5.3.0", "5.3.3"]:
        depends_on(f"mlirmiopen@{ver}", when=f"@{ver}")

    for ver in ["5.5.1", "5.6.0", "5.6.1", "5.7.0", "5.7.1", "6.0.0", "6.0.2", "6.1.0", "6.1.1"]:
        depends_on("nlohmann-json", type="link")
        depends_on(f"composable-kernel@{ver}", when=f"@{ver}")
    for ver in ["5.4.0", "5.4.3", "5.5.0"]:
        depends_on("nlohmann-json", type="link")
        depends_on(f"rocmlir@{ver}", when=f"@{ver}")
    for ver in ["6.0.0", "6.0.2", "6.1.0", "6.1.1"]:
        depends_on("roctracer-dev@" + ver, when="@" + ver)
    for ver in ["6.1.0", "6.1.1"]:
        depends_on("googletest")

    def setup_build_environment(self, env):
        lib_dir = self.spec["zlib-api"].libs.directories[0]
        env.prepend_path("LIBRARY_PATH", lib_dir)

    def get_bitcode_dir(self):
        return self.spec["llvm-amdgpu"].prefix.amdgcn.bitcode

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
        spec = self.spec

        args = [
            self.define("MIOPEN_BACKEND", "HIP"),
            self.define(
                "CMAKE_CXX_COMPILER", "{0}/bin/clang++".format(spec["llvm-amdgpu"].prefix)
            ),
            self.define(
                "MIOPEN_AMDGCN_ASSEMBLER", "{0}/bin/clang".format(spec["llvm-amdgpu"].prefix)
            ),
            self.define("Boost_USE_STATIC_LIBS", "Off"),
            self.define("HIP_PREFIX_PATH", spec["hip"].prefix),
            self.define("DEVICELIBS_PREFIX_PATH", self.get_bitcode_dir()),
        ]
        if self.spec.satisfies("@5.1.0:5.3"):
            mlir_inc = spec["mlirmiopen"].prefix.include
            args.append(self.define("CMAKE_CXX_FLAGS", "-I{0}".format(mlir_inc)))
        if self.spec.satisfies("@5.4.0:"):
            args.append(
                "-DNLOHMANN_JSON_INCLUDE={0}".format(self.spec["nlohmann-json"].prefix.include)
            )
        if self.spec.satisfies("@5.4.0:5.5.0"):
            args.append(self.define("MIOPEN_USE_COMPOSABLEKERNEL", "OFF"))
            args.append(self.define("MIOPEN_USE_MLIR", "ON"))
            args.append(self.define("MIOPEN_ENABLE_AI_KERNEL_TUNING", "OFF"))
        if self.spec.satisfies("@5.5.1:"):
            args.append(self.define("MIOPEN_USE_COMPOSABLEKERNEL", "ON"))
            args.append(self.define("MIOPEN_ENABLE_AI_KERNEL_TUNING", "OFF"))
            args.append(self.define("MIOPEN_USE_MLIR", "OFF"))
        if self.spec.satisfies("@5.7.0:"):
            args.append(self.define("MIOPEN_ENABLE_AI_IMMED_MODE_FALLBACK", "OFF"))
        args.append(
            "-DNLOHMANN_JSON_INCLUDE={0}".format(self.spec["nlohmann-json"].prefix.include)
        )
        if self.spec.satisfies("@6.0.0:"):
            args.append(
                "-DROCTRACER_INCLUDE_DIR={0}".format(self.spec["roctracer-dev"].prefix.include)
            )
            args.append("-DROCTRACER_LIB_DIR={0}".format(self.spec["roctracer-dev"].prefix.lib))
        if self.spec.satisfies("@6.1:"):
            args.append("-DSQLITE_INCLUDE_DIR={0}".format(self.spec["sqlite"].prefix.include))
        return args

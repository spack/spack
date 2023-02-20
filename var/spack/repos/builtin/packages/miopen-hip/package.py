# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re

from spack.package import *
from spack.pkg.builtin.boost import Boost


class MiopenHip(CMakePackage):
    """AMD's library for high performance machine learning primitives."""

    homepage = "https://github.com/ROCmSoftwarePlatform/MIOpen"
    git = "https://github.com/ROCmSoftwarePlatform/MIOpen.git"
    url = "https://github.com/ROCmSoftwarePlatform/MIOpen/archive/rocm-5.4.3.tar.gz"
    tags = ["rocm"]

    maintainers("srekolam", "renjithravindrankannath")
    libraries = ["libMIOpen"]

    version("5.4.3", sha256="37ffe2ed3d7942da8ea2f6bdb85c7a2f58e3ccd31767db158a322769d3604efd")
    version("5.4.0", sha256="b4153791f9eeee4cbc5534bc6ad8b32c0947bcd38e08b77ebe144065a4fa5456")
    version("5.3.3", sha256="7efc98215d23a2caaf212378c37e9a6484f54a4ed3e9660719286e4f287d3715")
    version("5.3.0", sha256="c5819f593d71beeda2eb24b89182912240cc40f83b2b8f9de695a8e230aa4ea6")
    version("5.2.3", sha256="28747847446955b3bab24f7fc65c1a6b863a12f12ad3a35e0312072482d38122")
    version("5.2.1", sha256="0977a8876d41bbd2fa268341c93892f35878d7efc1711194ad87582f877ff500")
    version("5.2.0", sha256="5fda69426e81df9f8fb6658e579176b9c4fcce3516fc8488d3cfd2b6f6f2b3b4")
    version("5.1.3", sha256="510461f5c5bdbcf8dc889099d1e5960b9f84bd845a9fc9154588a9898c701c1d")
    version("5.1.0", sha256="bb50201334d68addf153b84b88ab803027c4913d71bdbda6f5ccde3f672f6fdd")
    version(
        "5.0.2",
        sha256="e73c18c6e0791d6ca8958508d899072ce12fc6c27cf78792d0c2a5c7e34427be",
        deprecated=True,
    )
    version(
        "5.0.0",
        sha256="4a46a2bdd11a2597c83cdb0c5e208b81728fab2ff7c585dabfca5aa05ee7a4f7",
        deprecated=True,
    )
    version(
        "4.5.2",
        sha256="cb49bdf215ed9881755239b6312d72f829c1a0edf510e6d1fbb206c41f5406fc",
        deprecated=True,
    )
    version(
        "4.5.0",
        sha256="be2f5ce962e15e62d427978422498c0ddf821b91fd40777a1ba915a2794d6fda",
        deprecated=True,
    )
    version(
        "4.3.1",
        sha256="1fb2fd8b24f984174ec5338a58b7964e128b74dafb101373a41c8ed33955251a",
        deprecated=True,
    )
    version(
        "4.3.0",
        sha256="034445470cfd44480a1d9854f9fdfe92cfb8efa3f002dee508eb9585e338486d",
        deprecated=True,
    )
    version(
        "4.2.0",
        sha256="8ab02e784c8b3471159794766ed6303c333b33c69dc5186c0930e56504373b7c",
        deprecated=True,
    )
    version(
        "4.1.0",
        sha256="068b1bc33f90fe21d3aab5697d2b3b7b930e613c54d6c5ee820768579b2b41ee",
        deprecated=True,
    )
    version(
        "4.0.0",
        sha256="84c6c17be9c1a9cd0d3a2af283433f64b07a4b9941349f498e40fed82fb205a6",
        deprecated=True,
    )
    version(
        "3.10.0",
        sha256="926e43c5583cf70d6b247f9fe45971b8b1cc9668f9c8490c142c7e8b6e268f1a",
        deprecated=True,
    )
    version(
        "3.9.0",
        sha256="f57d75a220c1094395cc1dccab2185c759d779751ddbb5369a6f041ec77b2156",
        deprecated=True,
    )
    version(
        "3.8.0",
        sha256="612b30d4a967bf18c7fa7aa3ef12ed558314ed04cee2775b842bf6a96cd7276f",
        deprecated=True,
    )
    version(
        "3.7.0",
        sha256="f6a6ddd8d39bb76b7f7d91e68ade3b45e0201181145658c43b967065a354b103",
        deprecated=True,
    )
    version(
        "3.5.0",
        sha256="aa362e69c4dce7f5751f0ee04c745735ea5454c8101050e9b92cc60fa3c0fb82",
        deprecated=True,
    )

    variant(
        "build_type",
        default="Release",
        values=("Release", "Debug", "RelWithDebInfo"),
        description="CMake build type",
    )

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
    depends_on("zlib", when="@3.9.0:")

    patch("0001-Add-rocm-path-and-rocm-device-lib-path-flags.patch", when="@3.9.0:5.0.2")
    patch("miopen-hip-include-nlohmann-include-directory.patch", when="@5.4.0:")

    for ver in [
        "3.5.0",
        "3.7.0",
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
        depends_on("rocm-cmake@%s:" % ver, type="build", when="@" + ver)
        depends_on("hip@" + ver, when="@" + ver)
        depends_on("rocm-clang-ocl@" + ver, when="@" + ver)
        depends_on("rocblas@" + ver, when="@" + ver)

    for ver in ["5.1.0", "5.1.3", "5.2.0", "5.2.1", "5.2.3", "5.3.0", "5.3.3"]:
        depends_on("mlirmiopen@" + ver, when="@" + ver)

    for ver in ["5.4.0", "5.4.3"]:
        depends_on("rocmlir@" + ver, when="@" + ver)
        depends_on("nlohmann-json", type="link")

    def setup_build_environment(self, env):
        if "@3.9.0:" in self.spec:
            lib_dir = self.spec["zlib"].libs.directories[0]
            env.prepend_path("LIBRARY_PATH", lib_dir)

    def get_bitcode_dir(self):
        spec = self.spec

        # and the exact location of its bitcode depends on the version
        if spec.version >= Version("3.9.0"):
            return spec["llvm-amdgpu"].prefix.amdgcn.bitcode
        else:
            return spec["llvm-amdgpu"].prefix.lib

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
        # TODO: need to turn on composable-kernel to on at a later date
        # requires a new recipe for composable-kernel
        if self.spec.satisfies("@5.4.0:"):
            args.append(self.define("MIOPEN_USE_COMPOSABLEKERNEL", "OFF"))
            args.append(
                "-DNLOHMANN_JSON_INCLUDE={0}".format(self.spec["nlohmann-json"].prefix.include)
            )
        return args

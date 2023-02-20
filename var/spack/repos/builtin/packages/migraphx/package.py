# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re

from spack.package import *


class Migraphx(CMakePackage):
    """AMD's graph optimization engine."""

    homepage = "https://github.com/ROCmSoftwarePlatform/AMDMIGraphX"
    git = "https://github.com/ROCmSoftwarePlatform/AMDMIGraphX.git"
    url = "https://github.com/ROCmSoftwarePlatform/AMDMIGraphX/archive/rocm-5.4.3.tar.gz"
    tags = ["rocm"]

    maintainers("srekolam", "renjithravindrankannath")
    libraries = ["libmigraphx"]

    version("5.4.3", sha256="f83e7bbe5d6d0951fb2cf0abf7e8b3530e9a5e45f7cec6d760da055d6905d568")
    version("5.4.0", sha256="b6e7f4a1bf445ea0dae644ed5722369cde66fbee82a5917722f5d3f8c48b0a8c")
    version("5.3.3", sha256="91d91902bbedd5e1951a231e8e5c9a328360b128c731912ed17c8059df38e02a")
    version("5.3.0", sha256="d0b7283f42e03fb38b612868b8c94f46f27a6e0b019ae95fde5b9086582a1c69")
    version("5.2.3", sha256="03f7d49f2efdd2c7a6afcaa5a5db5103edc15047b0ff5e146a775cfb36b36af2")
    version("5.2.1", sha256="300d990e1b92ad27c3eba3e94ef34538730ca9556398b8b9f7d61d28bf66c57d")
    version("5.2.0", sha256="33afcdf52c6e0e3a2f939fcf30e87f712b8e8ef3633a3dc03a19fea359704925")
    version("5.1.3", sha256="686e068774500a46b6e6488370bbf5bd0bba6d19ecdb00636f951704d19c9ef2")
    version("5.1.0", sha256="6398efaef18a74f2a475aa21bd34bc7c077332a430ee3f6ba4fde6e6a6aa9f89")
    version(
        "5.0.2",
        sha256="3ef48ac03b909d1a1aa1f91f365ce64af2ce66635b6efb5ad0b207dc51ff2fd6",
        deprecated=True,
    )
    version(
        "5.0.0",
        sha256="779a91ccfa4c2576251189f0c646ff7707c3646319c7d5dd137872beb52d2953",
        deprecated=True,
    )
    version(
        "4.5.2",
        sha256="ecfd9a8e7967076f056d5b6a90b22f8919b82226443769b181193f16ebf58b83",
        deprecated=True,
    )
    version(
        "4.5.0",
        sha256="8d243a48406af7f960c03bc28a16fad931de8e008ae848799adae504cc5f1355",
        deprecated=True,
    )
    version(
        "4.3.1",
        sha256="e0b04da37aed937a2b2218059c189559a15460c191b5e9b00c7366c81c90b06e",
        deprecated=True,
    )
    version(
        "4.3.0",
        sha256="99cf202a5e86cf5502b0f8bf12f152dbd5a6aacc204b3d9d5efca67a54793408",
        deprecated=True,
    )
    version(
        "4.2.0",
        sha256="93f22f6c641dde5d7fb8abcbd99621b3c81e332e125a6f3a258d5e4cf2055f55",
        deprecated=True,
    )
    version(
        "4.1.0",
        sha256="f9b1d2e25cdbaf5d0bfb07d4c8ccef0abaa291757c4bce296c3b5b9488174045",
        deprecated=True,
    )
    version(
        "4.0.0",
        sha256="b8b845249626e9169353dbfa2530db468972a7569b248c8118ff19e029a12e55",
        deprecated=True,
    )
    version(
        "3.10.0",
        sha256="eda22b9af286afb7806e6b5d5ebb0d612dce87c9bad64ba5176fda1c2ed9c9b7",
        deprecated=True,
    )
    version(
        "3.9.0",
        sha256="7649689e06522302c07b39abb88bdcc3d4de18a7559d4f6a9e238e92b2074032",
        deprecated=True,
    )
    version(
        "3.8.0",
        sha256="08fa991349a2b95364b0a69be7960580c3e3fde2fda0f0c67bc41429ea2d67a0",
        deprecated=True,
    )
    version(
        "3.7.0",
        sha256="697c3c7babaa025eaabec630dbd8a87d10dc4fe35fafa3b0d3463aaf1fc46399",
        deprecated=True,
    )
    version(
        "3.5.0",
        sha256="5766f3b262468c500be5051a056811a8edfa741734a5c08c4ecb0337b7906377",
        deprecated=True,
    )

    def url_for_version(self, version):
        url = "https://github.com/ROCmSoftwarePlatform/AMDMIGraphX/archive/"
        if version <= Version("3.5.0"):
            url += "{0}.tar.gz".format(version)
        else:
            url += "rocm-{0}.tar.gz".format(version)

        return url

    variant(
        "build_type",
        default="Release",
        values=("Release", "Debug", "RelWithDebInfo"),
        description="CMake build type",
    )

    patch("0001-Adding-nlohmann-json-include-directory.patch", when="@3.9.0:")
    # Restrict Python 2.7 usage to fix the issue below
    # https://github.com/spack/spack/issues/24429
    patch("0002-restrict-python-2.7-usage.patch", when="@3.9.0:5.1.3")
    patch("0003-restrict-python-2.7-usage.patch", when="@5.2.0:")

    depends_on("cmake@3.5:", type="build")
    depends_on("protobuf", type="link")
    depends_on("blaze", type="build")
    depends_on("nlohmann-json", type="link")
    depends_on("msgpack-c", type="link")
    depends_on("half@1.12.0", type="link")
    depends_on("python@3.5:", type="build")
    depends_on("py-pybind11", type="build", when="@:4.0.0")
    depends_on("py-pybind11@2.6:", type="build", when="@4.1.0:")
    depends_on("pkgconfig", type="build", when="@5.3.0:")

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
        depends_on("llvm-amdgpu@" + ver, when="@" + ver)
        depends_on("rocblas@" + ver, when="@" + ver)
        depends_on("miopen-hip@" + ver, when="@" + ver)

    @property
    def cmake_python_hints(self):
        """Include the python include path to the
        CMake based on current spec
        """
        python = self.spec["python"]
        return [self.define("Python_INCLUDE_DIR", python.package.config_vars["include"])]

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
        args = ["-DCMAKE_CXX_COMPILER={0}/bin/clang++".format(self.spec["llvm-amdgpu"].prefix)]
        if "@3.9.0:" in self.spec:
            args.append(
                "-DNLOHMANN_JSON_INCLUDE={0}".format(self.spec["nlohmann-json"].prefix.include)
            )

        if self.spec["cmake"].satisfies("@3.16.0:"):
            args += self.cmake_python_hints
        return args

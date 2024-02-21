# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re

from spack.package import *


class RocprofilerDev(CMakePackage):
    """ROCPROFILER library for AMD HSA runtime API extension support"""

    homepage = "https://github.com/ROCm/rocprofiler"
    git = "https://github.com/ROCm/rocprofiler.git"
    url = "https://github.com/ROCm/rocprofiler/archive/refs/tags/rocm-5.4.3.tar.gz"
    tags = ["rocm"]

    maintainers("srekolam", "renjithravindrankannath")
    libraries = ["librocprofiler64"]
    license("MIT")
    version("5.4.3", sha256="86c3f43ee6cb9808796a21409c853cc8fd496578b9eef4de67ca77830229cac1")
    version("5.4.0", sha256="0322cbe5d1d3182e616f472da31f0707ad6040833c38c28f2b39381a85210f43")
    version("5.3.3", sha256="07ee28f3420a07fc9d45910e78ad7961b388109cfc0e74cfdf2666789e6af171")
    version("5.3.0", sha256="b0905a329dc1c97a362b951f3f8ef5da9d171cabb001ed4253bd59a2742e7d39")
    with default_args(deprecated=True):
        version("5.2.3", sha256="4ed22e86633ab177eed85fed8994fcb71017c4c4774998e4d3fc36b6c0a15eac")
        version("5.2.1", sha256="c6768ec428590aadfb0e7ef6e22b8dc5ac8ed97babeb56db07f2d5d41cd122e2")
        version("5.2.0", sha256="1f4db27b56ef1863d4c9e1d96bac9117d66be45156d0637cfe4fd38cae61a23a")
        version("5.1.3", sha256="eca7be451c7bf000fd9c75683e7f5dfbed32dbb385b5ac685d2251ee8c3abc96")
        version("5.1.0", sha256="4a1c6ed887b0159392406af8796508df2794353a4c3aacc801116044fb4a10a5")

    depends_on("cmake@3:", type="build")
    for ver in ["5.1.0", "5.1.3", "5.2.0", "5.2.1", "5.2.3", "5.3.0", "5.3.3", "5.4.0", "5.4.3"]:
        depends_on(f"hsakmt-roct@{ver}", when=f"@{ver}")
        depends_on(f"hsa-rocr-dev@{ver}", when=f"@{ver}")
        depends_on(f"rocminfo@{ver}", when=f"@{ver}")
        depends_on(f"roctracer-dev-api@{ver}", when=f"@{ver}")

    # See https://github.com/ROCm/rocprofiler/pull/50
    patch("fix-includes.patch")
    patch("0001-Continue-build-in-absence-of-aql-profile-lib.patch", when="@5.3:")

    def patch(self):
        filter_file(
            "${HSA_RUNTIME_LIB_PATH}/../include",
            "${HSA_RUNTIME_LIB_PATH}/../include ${HSA_KMT_LIB_PATH}/..\
                     /include",
            "test/CMakeLists.txt",
            string=True,
        )

    @classmethod
    def determine_version(cls, lib):
        match = re.search(r"lib\S*\.so\.\d+\.\d+\.(\d)(\d\d)(\d\d)", lib)
        if match:
            return "{0}.{1}.{2}".format(
                int(match.group(1)), int(match.group(2)), int(match.group(3))
            )
        return None

    def cmake_args(self):
        return [
            self.define(
                "PROF_API_HEADER_PATH", self.spec["roctracer-dev-api"].prefix.roctracer.include.ext
            ),
            self.define("ROCM_ROOT_DIR", self.spec["hsakmt-roct"].prefix.include),
        ]

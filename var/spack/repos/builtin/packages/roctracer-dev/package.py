# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re

from spack.package import *


class RoctracerDev(CMakePackage, ROCmPackage):
    """ROC-tracer library: Runtimes Generic Callback/Activity APIs.
    The goal of the implementation is to provide a generic independent from
    specific runtime profiler to trace API and asyncronous activity."""

    homepage = "https://github.com/ROCm-Developer-Tools/roctracer"
    git = "https://github.com/ROCm-Developer-Tools/roctracer.git"
    url = "https://github.com/ROCm-Developer-Tools/roctracer/archive/rocm-5.4.3.tar.gz"
    tags = ["rocm"]

    maintainers("srekolam", "renjithravindrankannath")
    libraries = ["libroctracer64"]

    version("5.4.3", sha256="6b5111be5efd4d7fd6935ca99b06fab19b43d97a58d26fc1fe6e783c4de9a926")
    version("5.4.0", sha256="04c1e955267a3e8440833a177bb976f57697aba0b90c325d07fc0c6bd4065aea")
    version("5.3.3", sha256="f2cb1e6bb69ea1a628c04f984741f781ae1d8498dc58e15795bb03015f924d13")
    version("5.3.0", sha256="36f1da60863a113bb9fe2957949c661f00a702e249bb0523cda1fb755c053808")
    version("5.2.3", sha256="93f4bb7529db732060bc12055aa10dc346a459a1086cddd5d86c7b509301be4f")
    version("5.2.1", sha256="e200b5342bdf840960ced6919d4bf42c8f30f8013513f25a2190ee8767667e59")
    version("5.2.0", sha256="9747356ce61c57d22c2e0a6c90b66a055e435d235ba3459dc3e3f62aabae6a03")
    version("5.1.3", sha256="45f19875c15eb609b993788b47fd9c773b4216074749d7744f3a671be17ef33c")
    version("5.1.0", sha256="58b535f5d6772258190e4adcc23f37c916f775057a91b960e1f2ee1f40ed5aac")
    version(
        "5.0.2",
        sha256="5ee46f079e57dfe491678ffa4cdaf5f3b3d179cb3137948e4bcafca99ded47cc",
        deprecated=True,
    )
    version(
        "5.0.0",
        sha256="a21f4fb093cee4a806d53cbc0645d615d89db12fbde305e9eceee7e4150acdf2",
        deprecated=True,
    )
    version(
        "4.5.2",
        sha256="7012d18b79736dbe119161aab86f4976b78553ce0b2f4753a9386752d75d5074",
        deprecated=True,
    )
    version(
        "4.5.0",
        sha256="83dcd8987e129b14da0fe74e24ce8d027333f8fedc9247a402d3683765983296",
        deprecated=True,
    )

    variant(
        "build_type",
        default="Release",
        values=("Release", "Debug", "RelWithDebInfo"),
        description="CMake build type",
    )

    depends_on("cmake@3:", type="build")
    depends_on("python@3:", type="build")
    depends_on("py-cppheaderparser", type="build")

    for ver in [
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
        depends_on("hsakmt-roct@" + ver, when="@" + ver)
        depends_on("hsa-rocr-dev@" + ver, when="@" + ver)
        depends_on("rocminfo@" + ver, when="@" + ver)
        depends_on("hip@" + ver, when="@" + ver)
        depends_on("rocprofiler-dev@" + ver, when="@" + ver)

    patch("0001-include-rocprofiler-dev-path.patch", when="@5.3:")

    @classmethod
    def determine_version(cls, lib):
        match = re.search(r"rocm-(\d+)\.(\d+)\.(\d)/lib/lib\S*\.so\.\d+\.\d+\.\d+", lib)
        if match:
            ver = "{0}.{1}.{2}".format(
                int(match.group(1)), int(match.group(2)), int(match.group(3))
            )
        else:
            ver = None
        return ver

    def patch(self):
        filter_file(
            "${CMAKE_PREFIX_PATH}/hsa",
            "${HSA_RUNTIME_INC_PATH}",
            "src/CMakeLists.txt",
            string=True,
        )
        kwargs = {"ignore_absent": False, "backup": False, "string": False}
        with working_dir("script"):
            match = "^#!/usr/bin/python[23]"
            python = self.spec["python"].command.path
            substitute = "#!{python}".format(python=python)
            files = ["check_trace.py", "gen_ostream_ops.py", "hsaap.py"]
            filter_file(match, substitute, *files, **kwargs)

    def cmake_args(self):
        args = [
            "-DHIP_VDI=1",
            "-DCMAKE_MODULE_PATH={0}/cmake_modules".format(self.stage.source_path),
            "-DHSA_RUNTIME_HSA_INC_PATH={0}/include".format(self.spec["hsa-rocr-dev"].prefix),
            "-DROCPROFILER_PATH={0}".format(self.spec["rocprofiler-dev"].prefix),
            "-DCMAKE_POSITION_INDEPENDENT_CODE:BOOL=ON",
        ]
        return args

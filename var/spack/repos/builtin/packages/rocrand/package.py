# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re

from spack.package import *


class Rocrand(CMakePackage):
    """The rocRAND project provides functions that generate
    pseudo-random and quasi-random numbers."""

    homepage = "https://github.com/ROCm/rocRAND"
    git = "https://github.com/ROCm/rocRAND.git"
    url = "https://github.com/ROCm/rocRAND/archive/rocm-6.0.2.tar.gz"
    tags = ["rocm"]

    maintainers("cgmb", "srekolam", "renjithravindrankannath")
    libraries = ["librocrand"]

    license("MIT")

    version("develop", branch="develop")
    version("master", branch="master")
    version("6.1.2", sha256="ac3c858c0f76188ac50574591aa6b41b27bda2af5925314451a44242319f28c8")
    version("6.1.1", sha256="d6302d014045694be85385cdc683ea75476e23fd92ae170079c261c0b041764b")
    version("6.1.0", sha256="ea80c5d657fa48b1122a47986239a04118977195ee4826d2b14b8bfe0fabce6e")
    version("6.0.2", sha256="51d66c645987cbfb593aaa6be94109e87fe4cb7e9c70309eb3c159af0de292d7")
    version("6.0.0", sha256="cee93231c088be524bb2cb0e6093ec47e62e61a55153486bebbc2ca5b3d49360")
    version("5.7.1", sha256="885cd905bbd23d02ba8f3f87d5c0b79bc44bd020ea9af190f3959cf5aa33d07d")
    version("5.7.0", sha256="d6053d986821e5cbc6cfec0778476efb1411ef943f11e7a8b973b1814a259dcf")
    with default_args(deprecated=True):
        version("5.6.1", sha256="6bf71e687ffa0fcc1b00e3567dd43da4147a82390f1b2db5e6f1f594dee6066d")
        version("5.6.0", sha256="cc894d2f1af55e16b62c179062063946609c656043556189c656a115fd7d6f5f")
        version("5.5.1", sha256="e8bed3741b19e296bd698fc55b43686206f42f4deea6ace71513e0c48258cc6e")
        version("5.5.0", sha256="0481e7ef74c181026487a532d1c17e62dd468e508106edde0279ca1adeee6f9a")

    amdgpu_targets = ROCmPackage.amdgpu_targets

    variant(
        "amdgpu_target",
        description="AMD GPU architecture",
        values=auto_or_any_combination_of(*amdgpu_targets),
        sticky=True,
    )

    depends_on("cmake@3.10.2:", type="build")

    depends_on("googletest@1.10.0:", type="test")

    for ver in [
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
        "6.1.2",
    ]:
        depends_on(f"hip@{ver}", when=f"@{ver}")
        depends_on(f"rocm-cmake@{ver}:", type="build", when=f"@{ver}")

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
        args = [self.define("BUILD_BENCHMARK", "OFF"), self.define("BUILD_TEST", self.run_tests)]

        if "auto" not in self.spec.variants["amdgpu_target"]:
            args.append(self.define_from_variant("AMDGPU_TARGETS", "amdgpu_target"))

        if self.spec.satisfies("^cmake@3.21.0:3.21.2"):
            args.append(self.define("__skip_rocmclang", "ON"))

        if self.spec.satisfies("@5.5.0:"):
            args.append(self.define("BUILD_HIPRAND", "OFF"))

        return args

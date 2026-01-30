# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.makefile import MakefilePackage

from spack.package import *


class FastqScan(MakefilePackage):
    """Fastq-scan reads a FASTQ from stdin and outputs summary statistics in JSON."""

    homepage = "https://github.com/rpetit3/fastq-scan"
    url = "https://github.com/rpetit3/fastq-scan/archive/refs/tags/v1.0.1.tar.gz"

    maintainers("josue-iac")

    license("MIT")

    version("1.0.1", sha256="b0b781cfac1e0fb90a432151c290f7e79a1af882f643406cc62ec8ec994fdf6d")
    version("1.0.0", sha256="3f1157196cf51294b421c640eb67593a059c8cee2f80f5479358c51f88f496c5")
    version("0.4.4", sha256="e05779660495b26af51de00562f6c28f2ab32be16794ea223ba82dc78d112ee1")
    version("0.4.3", sha256="4d0ff86d746040051f830697c0f793ba039b0a1f5eae6ef641406fe7551cf169")
    version("0.4.2", sha256="d991f6978f2fb05363cbf548d2c8396e52503c332e73c5159c2f1cb5228fb249")
    version("0.4.1", sha256="5fc4bf0b00da283a709c38c77fe4b30b98567cca9198fbdf033fd7aee2673032")
    version("0.4.0", sha256="45ca1fcc824c0abbc057cae190808c56f842b2d565f6ca7f2a4aac6372045c4e")
    version("0.3", sha256="e63cc9efa157e5dc65173b0fce1c87a8fdbaf7be2f493b6e1fc40d128510d101")
    version("0.2", sha256="0f5235fe6b358b29c7e9330e5db0ae5f25b01ddf6703426d6d8a529503d920cc")

    depends_on("zlib", type=("build", "link"))

    @property
    def build_targets(self):
        return ["CXX={0}".format(self.compiler.cxx), "all"]

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install("fastq-scan", prefix.bin)
        install("README.md", prefix)

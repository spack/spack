# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PikaAlgorithms(CMakePackage):
    """C++ parallel algorithms built on pika."""

    homepage = "https://github.com/pika-org/pika-algorithms/"
    url = "https://github.com/pika-org/pika-algorithms/archive/0.0.0.tar.gz"
    git = "https://github.com/pika-org/pika-algorithms.git"
    maintainers = ["msimberg", "albestro", "teonnik", "aurianer"]

    version("0.1.0", sha256="64da008897dfa7373155595c46d2ce6b97a8a3cb5bea33ae7f2d1ff359f0d9b6")
    version("main", branch="main")

    generator = "Ninja"

    map_cxxstd = lambda cxxstd: "2a" if cxxstd == "20" else cxxstd
    cxxstds = ("17", "20")
    variant(
        "cxxstd",
        default="17",
        values=cxxstds,
        description="Use the specified C++ standard when building",
    )

    # Build dependencies
    depends_on("git", type="build")
    depends_on("ninja", type="build")
    depends_on("cmake@3.22:", type="build")

    conflicts("%gcc@:8")
    conflicts("%clang@:8")

    # Other dependencies
    depends_on("boost@1.71:")
    depends_on("fmt@0.9:")
    depends_on("pika@0.11:")

    for cxxstd in cxxstds:
        depends_on("boost cxxstd={0}".format(map_cxxstd(cxxstd)), when="cxxstd={0}".format(cxxstd))
        depends_on("fmt cxxstd={0}".format(cxxstd), when="cxxstd={0}".format(cxxstd))
        depends_on("pika cxxstd={0}".format(cxxstd), when="cxxstd={0}".format(cxxstd))

    def cmake_args(self):
        return [
            self.define("PIKA_ALGORITHMS_WITH_CXX_STANDARD", self.spec.variants["cxxstd"].value)
        ]

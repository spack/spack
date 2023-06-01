# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import os

from spack.package import *


class Bedtools2(MakefilePackage):
    """Collectively, the bedtools utilities are a swiss-army knife of
    tools for a wide-range of genomics analysis tasks. The most
    widely-used tools enable genome arithmetic: that is, set theory
    on the genome."""

    homepage = "https://github.com/arq5x/bedtools2"
    url = "https://github.com/arq5x/bedtools2/archive/v2.30.0.tar.gz"

    version("2.31.0", sha256="183cf9a96aabc50ef4bd557a53fd01557a123c05a0dc87651371878f357439ec")
    version("2.30.0", sha256="c575861ec746322961cd15d8c0b532bb2a19333f1cf167bbff73230a7d67302f")
    version("2.29.2", sha256="bc2f36b5d4fc9890c69f607d54da873032628462e88c545dd633d2c787a544a5")
    version("2.27.1", sha256="edcac089d84e63a51f85c3c189469daa7d42180272130b046856faad3cf79112")
    version("2.27.0", sha256="e91390b567e577d337c15ca301e264b0355441f5ab90fa4f971622e3043e0ca0")
    version("2.26.0", sha256="15db784f60a11b104ccbc9f440282e5780e0522b8d55d359a8318a6b61897977")
    version("2.25.0", sha256="159122afb9978015f7ec85d7b17739b01415a5738086b20a48147eeefcf08cfb")
    version("2.23.0", sha256="9dacaa561d11ce9835d1d51e5aeb092bcbe117b7119663ec9a671abac6a36056")
    version("2.21.0", sha256="51380b718cc5f2023d0738374a86a7d42fcca2385cf051a6f0c95d9c2624d78d")

    depends_on("zlib")
    depends_on("bzip2", when="@2.29:")
    depends_on("xz", when="@2.29:")
    depends_on("python", type="build")
    depends_on("samtools", type="test")

    conflicts(
        "%gcc@11:",
        when="@:2.26.0",
        msg="bedtools2 2.26.0 and earlier requires GCC 10 or earlier to build",
    )

    # https://github.com/arq5x/bedtools2/commit/58e9973af1b3f5e3b26e5584aad7dc7b720f8765
    patch("fix-binary-variable.patch", when="@:2.29.2")
    # https://github.com/arq5x/bedtools2/commit/ed59faae0cdd9e1676f57666613ac372366227e9
    patch("fix-broken-test.patch", when="@:2.24.0")
    # https://github.com/arq5x/bedtools2/issues/84
    # https://github.com/arq5x/bedtools2/issues/85
    patch("remove-unreproducible-tests.patch", when="@:2.24.0")

    @when("@2.22.1:")
    def install(self, spec, prefix):
        make("prefix=%s" % prefix, "install")

    @when("@:2.22.0")
    def install(self, spec, prefix):
        mkdir(prefix.bin)
        install_tree("bin", prefix.bin)

    @run_after("install")
    def cache_test_sources(self):
        self.cache_extra_test_sources(["test"])
        self.cache_extra_test_sources(["data"])
        self.cache_extra_test_sources(["genomes"])

    def test(self):
        test_dir = join_path(self.test_suite.current_test_cache_dir, "test")

        if not os.path.exists(test_dir):
            print("skipping all tests")
            return

        # BT=${BT-../../bin/bedtools}
        os.environ["BT"] = "bedtools"

        self.run_test(
            "bash", options=["test.sh"], purpose="test: run all tests", work_dir=test_dir
        )

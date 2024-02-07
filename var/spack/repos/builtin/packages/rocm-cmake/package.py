# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class RocmCmake(CMakePackage):
    """rocm-cmake provides CMake modules for common build tasks
    in the ROCm software stack"""

    homepage = "https://github.com/ROCm/rocm-cmake"
    git = "https://github.com/ROCm/rocm-cmake.git"
    url = "https://github.com/ROCm/rocm-cmake/archive/rocm-5.6.0.tar.gz"
    tags = ["rocm"]

    maintainers("srekolam", "renjithravindrankannath")

    license("MIT")

    version("master", branch="master")
    version("6.0.2", sha256="7bd3ff971b1a898b8cf06b0ed9fac45891e2523ae651c3194ba36050ab45f869")
    version("6.0.0", sha256="82bd97ba23d1883ef38bb667e92f7367fedc50d6c11c82f54cced4ab04b0412d")
    version("5.7.1", sha256="4a4c6aa09576ccb834f869bdcb49e98cc0f0bac3678b802358065d1179a9d6f1")
    version("5.7.0", sha256="93b98144201a1143eeca32744a9927d063f4685189f132ba52a6f3bba158a86b")
    version("5.6.1", sha256="98bf5fe2e6e12f55d122807d0060f1bb19c80d63d2c2f6fee579c40bfd244fa6")
    version("5.6.0", sha256="a118ca937856a4d0039955a8aef2466ef1fd1f08f7f7221cda53e1b5d02e476a")
    version("5.5.1", sha256="60113412b35d94e20e8100ed3db688c35801991b4b8fa282fdc6fd6fd413fb6e")
    version("5.5.0", sha256="b7884c346737eba70ae11044e41598b2482a92e21f3e0719b1ca11619f02a20b")
    version("5.4.3", sha256="c185b3a10d191d73b76770ca0f9d6bdc355ee91fe0c9016a3779c9cfe042ba0f")
    version("5.4.0", sha256="617faa9a1e51db3c7a59bd0393e054ab67e57be357d59cb0cd9b677f47824946")
    version("5.3.3", sha256="3e527f99db52e301ab4f1b994029585951e2ae685f0cdfb7b8529c72f4b77af4")
    version("5.3.0", sha256="659a8327f13e6786103dd562d3632e89a51244548fca081f46c753857cf09d04")
    version("5.2.3", sha256="c63b707ec07d24fda5a2a6fffeda4df4cc04ceea5df3b8822cbe4e6600e358b4")
    version("5.2.1", sha256="3d179496fb8f5f96230f736a313990f66705dc91fd10948a3042b495a440bf63")
    version("5.2.0", sha256="be8646c4f7babfe9a103c97d0e9f369322f8ac6cfa528edacdbdcf7f3ef44943")
    version("5.1.3", sha256="19b2da0d56300aab454655b57435ab3ed9e101ecb96561336ea8865bbd993c23")
    version("5.1.0", sha256="2eff47b7cf5bd56d465ff3c110eb936d31860df60182a82ba511ba11bbcf23fc")
    version(
        "5.0.2",
        sha256="86a4ae0f84dcf5be95a252295eb732d6a7a271297eed37800a9d492c16474d0c",
        deprecated=True,
    )
    version(
        "5.0.0",
        sha256="45eb958fac33aafea86fb498127ebf8f567646ce9d7288d46afbd087500553a1",
        deprecated=True,
    )
    version(
        "4.5.2",
        sha256="85f2ef51327e4b09d81a221b4ad31c97923dabc1bc8ff127dd6c570742185751",
        deprecated=True,
    )
    version(
        "4.5.0",
        sha256="c77b71454010adbeea5357773aa98dd0725f655f51a411815807cabf29258395",
        deprecated=True,
    )
    version(
        "4.3.1",
        sha256="acf2a58e2cd486f473194bf01247c52dbf20bd5f6465810fb221470298f2557f",
        deprecated=True,
    )
    version(
        "4.3.0",
        sha256="bb752d8d2727b7ef2754838e389075dd4212cf5439d099392141f93d05391415",
        deprecated=True,
    )
    version(
        "4.2.0",
        sha256="299e190ec3d38c2279d9aec762469628f0b2b1867adc082edc5708d1ac785c3b",
        deprecated=True,
    )
    version(
        "4.1.0",
        sha256="a4521d119fa07954e529d5e717ad1b338992c0694690dbce00fee26c01129c8c",
        deprecated=True,
    )
    version(
        "4.0.0",
        sha256="4577487acaa6e041a1316145867584f31caaf0d4aa2dd8fd7f82f81c269cada6",
        deprecated=True,
    )
    version(
        "3.10.0",
        sha256="751be4484efdcf0d5fa675480db6e2cddab897de4708c7c7b9fa7adb430b52d7",
        deprecated=True,
    )
    version(
        "3.9.0",
        sha256="e0a8db85bb55acb549f360eb9b04f55104aa93e4c3db33f9ba11d9adae2a07eb",
        deprecated=True,
    )
    version(
        "3.8.0",
        sha256="9e4be93c76631224eb49b2fa30b0d14c1b3311a6519c8b393da96ac0649d9f30",
        deprecated=True,
    )
    version(
        "3.7.0",
        sha256="51abfb06124c2e0677c4d6f7fe83c22fe855cb21386f0053ace09f8ab297058b",
        deprecated=True,
    )
    version(
        "3.5.0",
        sha256="5fc09e168879823160f5fdf4fd1ace2702d36545bf733e8005ed4ca18c3e910f",
        deprecated=True,
    )

    depends_on("cmake@3:", type="build")
    depends_on("cmake@3.6:", type="build", when="@4.1.0:")

    for ver in ["5.5.0", "5.5.1", "5.6.0", "5.6.1", "5.7.0", "5.7.1", "6.0.0"]:
        depends_on("rocm-core@" + ver, when="@" + ver)

    test_src_dir = "test"

    @run_after("install")
    def cache_test_sources(self):
        """Copy the tests source files after the package is installed to an
        install test subdirectory for use during `spack test run`."""
        if self.spec.satisfies("@:5.1.0"):
            return
        self.cache_extra_test_sources([self.test_src_dir])

    def test(self):
        if self.spec.satisfies("@:5.1.0"):
            print("Skipping: stand-alone tests")
            return
        test_dir = join_path(self.test_suite.current_test_cache_dir, self.test_src_dir)
        with working_dir(test_dir, create=True):
            cmake_bin = join_path(self.spec["cmake"].prefix.bin, "cmake")
            prefixes = ";".join([self.spec["rocm-cmake"].prefix])
            cc_options = ["-DCMAKE_PREFIX_PATH=" + prefixes, "."]
            self.run_test(cmake_bin, cc_options)
            make()
            make("clean")

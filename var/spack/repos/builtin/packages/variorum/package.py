# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Variorum(CMakePackage):
    """Variorum is a library providing vendor-neutral interfaces for
       monitoring and controlling underlying hardware features.
    """

    homepage = "https://variorum.readthedocs.io"
    git = "https://github.com/llnl/variorum.git"
    url = "https://github.com/llnl/variorum/archive/v0.1.0.tar.gz"

    maintainers = ["slabasan", "rountree"]

    version('0.4.1', sha256='be7407b856bc2239ecaa27d3df80aee2f541bb721fbfa183612bd9c0ce061f28')
    version('0.4.0', sha256='70ff1c5a3ae15d0bd07d409ab6f3c128e69528703a829cb18ecb4a50adeaea34')
    version('0.3.0', sha256='f79563f09b8fe796283c879b05f7730c36d79ca0346c12995b7bccc823653f42')
    version('0.2.0', sha256='b8c010b26aad8acc75d146c4461532cf5d9d3d24d6fc30ee68f6330a68e65744')
    version("0.1.0", tag="v0.1.0")

    ############
    # Variants #
    ############
    variant("shared", default=True, description="Build Variorum as shared lib")
    variant("docs", default=False,
            description="Build Variorum's documentation")
    variant("log", default=False, description="Enable Variorum's logs")
    variant("build_type", default="Release",
            description="CMake build type",
            values=("Debug", "Release"))

    ########################
    # Package dependencies #
    ########################
    depends_on("cmake@2.8:", type="build")
    depends_on("hwloc")

    #########################
    # Documentation related #
    #########################
    depends_on("py-sphinx", when="+docs", type="build")

    root_cmakelists_dir = "src"

    def cmake_args(self):
        spec = self.spec
        cmake_args = []

        if "+shared" in spec:
            cmake_args.append("-DBUILD_SHARED_LIBS=ON")
        else:
            cmake_args.append("-DBUILD_SHARED_LIBS=OFF")

        if "+docs" in spec:
            cmake_args.append("-DBUILD_DOCS=ON")
            sphinx_build_exe = join_path(
                spec["py-sphinx"].prefix.bin,
                "sphinx-build"
            )
            cmake_args.append("-DSPHINX_EXECUTABLE=" + sphinx_build_exe)
        else:
            cmake_args.append("-DBUILD_DOCS=OFF")

        if 'build_type=Debug' in spec:
            cmake_args.append("-DVARIORUM_DEBUG=ON")
        else:
            cmake_args.append("-DVARIORUM_DEBUG=OFF")

        if "+log" in spec:
            cmake_args.append("-DVARIORUM_LOG=ON")
        else:
            cmake_args.append("-DVARIORUM_LOG=OFF")

        if self.run_tests:
            cmake_args.append("-DBUILD_TESTS=ON")
        else:
            cmake_args.append("-DBUILD_TESTS=OFF")

        return cmake_args

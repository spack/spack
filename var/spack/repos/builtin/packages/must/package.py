# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Must(CMakePackage):
    """MUST detects usage errors of the Message Passing Interface (MPI)
    and reports them to the user. As MPI calls are complex and usage
    errors common, this functionality is extremely helpful for application
    developers that want to develop correct MPI applications. This includes
    errors that already manifest: segmentation faults or incorrect results
    as well as many errors that are not visible to the application developer
    or do not manifest on a certain system or MPI implementation."""

    homepage = "https://www.i12.rwth-aachen.de/go/id/nrbe"
    url = "https://hpc.rwth-aachen.de/must/files/MUST-v1.8.0-rc1.tar.gz"

    maintainers("jgalarowicz", "dmont")

    version("1.8.0-rc1", sha256="49fd2487fbd1aa41f4252c7e37efebd3f6ff48218c88e82f34b88d59348fe406")
    version(
        "1.8-preview", sha256="67b4b061db7a893e22a6610e2085072716d11738bc6cc3cb3ffd60d6833e8bad"
    )
    version("1.7.2", sha256="616c54b7487923959df126ac4b47ae8c611717d679fe7ec29f57a89bf0e2e0d0")
    variant("test", default=False, description="Enable must internal tests")
    variant("tsan", default=True, description="Enable thread sanitizer")
    variant("graphviz", default=False, description="Use to generate graphs")
    variant("stackwalker", default=False, description="Unwind with stackwalker")
    variant("backward", default=True, description="Unwind with backward-cpp")
    variant("typeart", default=False, description="Enable TypeArt build")

    # Don't enable stackwalker, backward simultaneously
    # Use either backward or stackwalker for unwinding
    conflicts("+stackwalker +backward")

    depends_on("cmake@3.9:")
    depends_on("python@3.1.5:", type=("build", "link", "run"))
    # must test variant requires llvm
    depends_on("llvm@10.0.0:", when="+test")
    # must typeart typeart variant requires llvm
    depends_on("llvm@10.0.0:", when="+typeart")
    depends_on("mpi")
    depends_on("libxml2")
    depends_on("dyninst", when="+stackwalker")
    depends_on("graphviz", when="+graphviz")

    @run_after("install")
    def install_prebuilds(self):
        """Perform make install-prebuilds"""
        with working_dir(self.build_directory):
            make("prebuilds")
            make("install-prebuilds")

    #
    # Set up the arguments to cmake for the build of must
    #
    def cmake_args(self):
        spec = self.spec

        # Add in paths for finding package config files that tell us
        # where to find these packages
        cmake_args = ["-DCMAKE_VERBOSE_MAKEFILE=ON", "-DCMAKE_BUILD_TYPE=Release"]

        # check to see if the testing variant is enabled
        if spec.satisfies("+test"):
            cmake_args.extend(["-DENABLE TESTS=On"])

        # check to see if the TypeArt variant is enabled
        if spec.satisfies("+typeart"):
            cmake_args.extend(["-DENABLE TYPEART=On"])

        # check to see if the Thread Sanitizer variant is enabled
        if spec.satisfies("+tsan"):
            cmake_args.extend(["-DENABLE TSAN=On"])
        else:
            # if the Thread Sanitizer variant is disabled
            # send corresponding cmake argument to the cmake command
            if spec.satisfies("~tsan"):
                cmake_args.extend(["-DENABLE TSAN=Off"])

        # Since MUST version 1.8, MUST is configured with
        # backward-cpp support enabled by default. To install
        # MUST without backward-cpp support, the CMake variable
        # -DUSE BACKWARD=Off must be explicitly set during the
        # configuration of MUST
        if spec.satisfies("~backward"):
            cmake_args.extend(["-DUSE BACKWARD=Off"])

        if spec.satisfies("+stackwalker"):
            cmake_args.extend(["-DUSE CALLPATH=On"])
            cmake_args.extend(["-DSTACKWALKER INSTALL PREFIX=%s" % spec["dyninst"].prefix])
            cmake_args.extend(["-DUSE BACKWARD=Off"])
        else:
            if spec.satisfies("+backward"):
                cmake_args.extend(["-DUSE BACKWARD=On"])

        return cmake_args

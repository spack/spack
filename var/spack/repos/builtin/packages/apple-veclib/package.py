# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class AppleVeclib(BundlePackage):
    """Shim package for the core OpenGL library from Apple"""
    homepage = "https://developer.apple.com/documentation/accelerate"
    maintainers("elfprince13")

    version("1068.60") # Sequoia 15.3.1

    provides("blas")
    # according to https://developer.apple.com/documentation/accelerate/blas-library
    # there's even a way to get lapack 3.12.0 but start with the bare minimum to get
    # this working
    provides("lapack@3.9.1",when="@1068.60:")

    requires(
        "platform=darwin",
        msg="Apple vecLib is only available on Darwin",
    )

    def setup_dependent_build_environment(self, env, dependent_spec):
        # we try to setup a build environment with enough hints
        # for the build system to pick up on the Apple framework version
        # of vecLib.
        # # - for a cmake build we actually needs nothing at all as
        # # find_package(OpenGL) will do the right thing
        # # - for the rest of the build systems we'll assume that
        # # setting the C_INCLUDE_PATH will be enough for the compilation phase
        # # and *** for the link phase.
        # env.prepend_path("C_INCLUDE_PATH", self.prefix[:-4])
        pass

    @property
    def headers(self):
        return HeaderList(
            join_path(self.prefix, "System/Library/Frameworks/Accelerate.framework/Frameworks/vecLib.Framework/Headers")
        )

    @property
    def libs(self):
        return LibraryList(join_path(self.prefix, "System/Library/Frameworks/Accelerate.framework/Frameworks/vecLib.Framework"))

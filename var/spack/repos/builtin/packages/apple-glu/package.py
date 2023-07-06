# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class AppleGlu(Package):
    """Shim package for Apple implementation of OpenGL Utility Libray (GLU)"""

    homepage = "https://developer.apple.com/library/archive/documentation/GraphicsImaging/Conceptual/OpenGL-MacProgGuide/opengl_intro/opengl_intro.html"

    maintainers("aphecetche")

    has_code = False

    version("1.3.0")

    provides("glu@1.3")

    # Only supported on 'platform=darwin' and compiler=apple-clang
    conflicts("platform=linux")
    conflicts("platform=cray")
    conflicts("%gcc")
    conflicts("%clang")

    phases = []

    def setup_dependent_build_environment(self, env, dependent_spec):
        # we try to setup a build environment with enough hints
        # for the build system to pick up on the Apple framework version
        # of OpenGL.
        # - for a cmake build we actually needs nothing at all as
        # find_package(OpenGL) will do the right thing
        # - for the rest of the build systems we'll assume that
        # setting the C_INCLUDE_PATH will be enough for the compilation phase
        # and *** for the link phase.
        env.prepend_path("C_INCLUDE_PATH", self.prefix[:-4])

    @property
    def headers(self):
        return HeaderList(
            join_path(self.prefix, "System/Library/Frameworks/OpenGL.framework/Headers")
        )

    @property
    def libs(self):
        return LibraryList(join_path(self.prefix, "System/Library/Frameworks/OpenGL.framework"))

# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class HealpixCxx(AutotoolsPackage):
    """Healpix-CXX is a C/C++ library for calculating
    Hierarchical Equal Area isoLatitude Pixelation of a sphere."""

    homepage = "https://healpix.sourceforge.io"

    version("3.82.0", sha256="9c1b0bbbcf007359d1ef10ae3ae9a2f46c72a4eb0c2fdbb43683289002ba8552")
    version("3.50.0", sha256="6538ee160423e8a0c0f92cf2b2001e1a2afd9567d026a86ff6e2287c1580cb4c")

    depends_on("cfitsio")
    depends_on("libsharp", when="@3.50.0")
    depends_on("libsharp2", when="@3.82.0:")

    def url_for_version(self, version):
        major, minor, patch = version
        return f"https://sourceforge.net/projects/healpix/files/Healpix_{major}.{minor}/healpix_cxx-{major}.{minor}.{patch}.tar.gz/download"

    @when("@3.82.0:")
    def setup_build_environment(self, env):
        env.set("SHARP_CFLAGS", "-I{0}".format(self.spec["libsharp2"].prefix.include))
        env.set("SHARP_LIBS", "-L{0} -lsharp".format(self.spec["libsharp2"].prefix.lib))

    @when("@3.50.0")
    def patch(self):
        spec = self.spec
        configure_fix = FileFilter("configure")
        # Link libsharp static libs
        configure_fix.filter(
            r"^SHARP_LIBS=.*$",
            'SHARP_LIBS="-L{0} -lsharp -lc_utils -lfftpack -lm"'.format(
                spec["libsharp"].prefix.lib
            ),
        )

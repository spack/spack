# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Babl(MesonPackage):
    """babl is pixel encoding and color space conversion engine in C.

    It allows converting between different methods of storing pixels
    known as pixel formats that have with different bitdepths and
    other data representations, color models, color spaces and
    component permutations."""

    homepage = "https://gegl.org/babl"
    url = "https://download.gimp.org/babl/0.1/babl-0.1.98.tar.xz"

    maintainers("benkirk")

    version("0.1.98", sha256="f3b222f84e462735de63fa9c3651942f2b78fd314c73a22e05ff7c73afd23af1")
    version("0.1.96", sha256="33673fe459a983f411245a49f81fd7f1966af1ea8eca9b095a940c542b8545f6")
    version("0.1.94", sha256="b6a8b28f55e0c17f5031fb7959e72ffe0fbf8196d1968ad6efc98d1b492c3bbe")
    version("0.1.92", sha256="f667735028944b6375ad18f160a64ceb93f5c7dccaa9d8751de359777488a2c1")
    version("0.1.90", sha256="6e2ebb636f37581588e3d02499b3d2f69f9ac73e34a262f42911d7f5906a9243")

    depends_on("cmake@3.4:", type="build")
    depends_on("lcms")
    depends_on("gobject-introspection")

    def setup_dependent_build_environment(self, env, dependent_spec):
        env.prepend_path("XDG_DATA_DIRS", self.prefix.share)

    def setup_dependent_run_environment(self, env, dependent_spec):
        env.prepend_path("XDG_DATA_DIRS", self.prefix.share)

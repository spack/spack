# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class PyNinja(PythonPackage):
    """Ninja is a small build system with a focus on speed."""

    homepage = "https://ninja-build.org"
    pypi = "ninja/ninja-1.10.2.tar.gz"

    version("1.11.1", sha256="c833a47d39b2d1eee3f9ca886fa1581efd5be6068b82734ac229961ee8748f90")
    version("1.10.2.4", sha256="da7a6d9b2ed2018165fbf90068e2c64da08f2568c700fdb8abea07a245dc4664")
    version("1.10.2.3", sha256="e1b86ad50d4e681a7dbdff05fc23bb52cb773edb90bc428efba33fa027738408")
    version("1.10.2.2", sha256="3f8a75acd929abb9f003d3aa5bc299cea30b9db0dfa18669877e9c02ddcf530d")
    version("1.10.2.1", sha256="719ab357f5dc822711c1151d1b9517c5543340e23f6cc4e8508f793848a48bb1")
    version("1.10.2", sha256="bb5e54b9a7343b3a8fc6532ae2c169af387a45b0d4dd5b72c2803e21658c5791")

    depends_on("cmake@3.6:", type="build")
    depends_on("py-setuptools@42:", type="build")
    depends_on("py-scikit-build", type="build")
    depends_on("ninja@1.10.2", type=("build", "run"))

    def patch(self):
        os.unlink(join_path(self.stage.source_path, "CMakeLists.txt"))

    @run_after("install")
    def installit(self):
        syntax_file = os.path.join(self.spec["ninja"].prefix.misc, "ninja_syntax.py")
        bin_file = os.path.join(self.spec["ninja"].prefix.bin, "ninja")
        dst = os.path.join(python_platlib, "ninja")
        dstbin = os.path.join(dst, "data", "bin")
        mkdirp(dstbin)
        os.symlink(bin_file, os.path.join(dstbin, "ninja"))
        os.symlink(syntax_file, os.path.join(dst, "ninja_syntax.py"))

# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class SpiralPackageJit(Package):
    """This is the SPIRAL package for Just-In-Time (JIT) or Real-Time 
    Compilation (RTC)."""

    homepage = "https://spiralgen.com"
    url = "https://github.com/spiral-software/spiral-package-jit/archive/refs/tags/1.0.1.tar.gz"
    git = "https://github.com/spiral-software/spiral-package-jit.git"

    maintainers("spiralgen")
    extends("spiral-software")

    version("develop", branch="develop")
    version("main", branch="main")
    version("1.0.1", sha256="acf22db04e705276f06642d7f2ebf161f6c347f93bb1bdd6e3ddcfc4b7be5707")

    # JIT package is an extension for Spiral (spec: spiral-software).  Spiral finds
    # extensions in the "namespaces/packages" folder.  Install the tree in a similarly
    # named folder so that when activated it'll get symlinked to the correct place.

    def install(self, spec, prefix):
        spiral_pkgs = join_path(prefix, "namespaces", "packages", "jit")
        install_tree(".", spiral_pkgs)

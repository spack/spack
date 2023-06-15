# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Nvtx(Package, PythonExtension):
    
    git = "https://github.com/NVIDIA/NVTX.git"
    url = "https://github.com/NVIDIA/NVTX/archive/refs/tags/v3.1.0.tar.gz"
    
    maintainers("thomas-bouvier")

    version("main", branch="dev")
    version("3.1.0", sha256="dc4e4a227d04d3da46ad920dfee5f7599ac8d6b2ee1809c9067110fb1cc71ced")

    variant("python", default=True, description="Install python bindings.")
    extends("python", when="+python")
    depends_on("py-setuptools", type="build", when="+python")
    depends_on("py-wheel", type="build", when="+python")
    depends_on("py-cython", type="build", when="+python")

    #depends_on("cmake@3.10:", type="build")
    #root_cmakelists_dir = "c"
    #install_targets = []

    build_directory = 'python'

    def install(self, spec, prefix):
        install_tree('c/include', prefix.include)
        install('./LICENSE.txt', "%s" % prefix)

    @run_after("install")
    def install_python(self):
        """Install everything from build directory."""
        pass
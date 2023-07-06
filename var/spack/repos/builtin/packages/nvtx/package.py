# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Nvtx(Package, PythonExtension):
    """Python code annotation library"""

    git = "https://github.com/NVIDIA/NVTX.git"
    url = "https://github.com/NVIDIA/NVTX/archive/refs/tags/v3.1.0.tar.gz"

    maintainers("thomas-bouvier")

    version("develop", branch="dev")
    version("3.1.0", sha256="dc4e4a227d04d3da46ad920dfee5f7599ac8d6b2ee1809c9067110fb1cc71ced")

    variant("python", default=True, description="Install Python bindings.")
    extends("python", when="+python")
    depends_on("py-pip", type="build", when="+python")
    depends_on("py-setuptools", type="build", when="+python")
    depends_on("py-wheel", type="build", when="+python")
    depends_on("py-cython", type="build", when="+python")

    build_directory = "python"

    # Create a nvtx-config.cmake file to make calls to find_package(nvtx) to
    # work as expected
    patch("nvtx-config.patch")

    def patch(self):
        """Patch setup.py to provide include directory."""
        include_dir = prefix.include
        setup = FileFilter("python/setup.py")
        setup.filter("include_dirs=include_dirs", f"include_dirs=['{include_dir}']", string=True)

    def install(self, spec, prefix):
        install_tree("c/include", prefix.include)
        install("c/CMakeLists.txt", prefix)
        install("c/nvtxImportedTargets.cmake", prefix)
        install("./LICENSE.txt", prefix)

        install("./nvtx-config.cmake", prefix)  # added by the patch above

        args = std_pip_args + ["--prefix=" + prefix, "."]
        with working_dir(self.build_directory):
            pip(*args)

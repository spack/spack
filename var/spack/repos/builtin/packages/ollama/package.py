# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install ollama
#
# You can edit this file again by typing:
#
#     spack edit ollama
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------
import spack.build_systems.go
from spack.package import *


class Ollama(GoPackage):
    """Run Llama 2, Code Llama, and other models. Customize and create your own."""

    homepage = "https://ollama.com"
    git = "https://github.com/ollama/ollama.git"

    maintainers("teaguesterling")

    version("0.1.31", commit="dc011d16b9ff160c0be3829fc39a43054f0315d0", submodules=True)

    depends_on("cmake", type="build")
    depends_on("go", type="build")
    depends_on("gcc", type="build")
    depends_on("git", type="build")
    depends_on("ccache", type="build")


class GoBuilder(spack.build_systems.go.GoBuilder):
    phases = ("generate", "build", "install")

    @property
    def generate_args(self):
        """Arguments for ``go generate``."""
        return ["./..."]

    def generate(self, pkg, spec, prefix):
        """Runs ``go generate`` in the source directory"""
        import inspect, llnl.util.filesystem as fs
        with fs.working_dir(self.build_directory):
            inspect.getmodule(pkg).go("generate", *self.generate_args)


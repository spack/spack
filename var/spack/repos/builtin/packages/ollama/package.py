# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import spack.build_systems.go
from spack.package import *


class Ollama(GoPackage):
    """Run Llama 2, Code Llama, and other models. Customize and create your own."""

    homepage = "https://ollama.com"
    git = "https://github.com/ollama/ollama.git"

    maintainers("teaguesterling")

    # We're using commit IDs because the `go generate` process will fail for some
    # dependencies that expect to be within a git repo. This is also an issue with
    # cached downloads, but I don't know how to fix that yet
    version("0.1.31", commit="dc011d16b9ff160c0be3829fc39a43054f0315d0", submodules=True)
    # This is the last verified non-preview version as of 20240413
    version(
        "0.1.30",
        commit="756c2575535641f1b96d94b4214941b90f4c30c7",
        submodules=True,
        preferred=True,
    )

    license("MIT", checked_by="teaguesterling")

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
        import inspect

        import llnl.util.filesystem as fs

        with fs.working_dir(self.build_directory):
            inspect.getmodule(pkg).go("generate", *self.generate_args)

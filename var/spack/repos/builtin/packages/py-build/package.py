# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import glob
import os

from spack.package import *


class PyBuild(Package, PythonExtension):
    """A simple, correct Python build frontend."""

    homepage = "https://github.com/pypa/build"
    url = "https://files.pythonhosted.org/packages/source/b/build/build-0.10.0.tar.gz"
    list_url = "https://pypi.org/simple/build/"

    version("0.10.0", sha256="d5b71264afdb5951d6704482aac78de887c80691c52b88a9ad195983ca2c9269")

    extends("python")
    depends_on("py-installer", type="build")

    depends_on("py-flit-core@3.4:", type="build")
    depends_on("py-packaging@19:", type=("build", "run"))
    depends_on("py-pyproject-hooks", type=("build", "run"))
    depends_on("py-colorama", when="platform=windows", type=("build", "run"))
    depends_on("py-importlib-metadata@0.22:", when="^python@:3.7", type=("build", "run"))
    depends_on("py-tomli@1.1:", when="^python@:3.10", type=("build", "run"))

    # https://github.com/pypa/build/issues/266
    # https://github.com/pypa/build/issues/406
    patch("isolation.patch")

    def setup_build_environment(self, env):
        # To build build from source, we need to use build to bootstrap itself
        env.prepend_path("PYTHONPATH", "src")

    def install(self, spec, prefix):
        python("-m", "build", "--no-isolation", ".")
        wheel = glob.glob(os.path.join("dist", "*.whl"))[0]
        installer("--prefix", prefix, wheel)

    def setup_dependent_package(self, module, dependent_spec):
        build = dependent_spec["python"].command
        build.add_default_arg("-m")
        build.add_default_arg("build")
        setattr(module, "build", build)

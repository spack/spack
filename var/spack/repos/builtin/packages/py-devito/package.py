# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDevito(PythonPackage):
    """Devito is a Python package to implement optimized stencil computation.

    (e.g., finite differences, image processing, machine learning) from high-level
    symbolic problem definitions. Devito builds on SymPy and employs automated code
    generation and just-in-time compilation to execute optimized computational kernels
    on several computer platforms, including CPUs, GPUs, and clusters thereof.
    """

    homepage = "https://www.devitoproject.org/"
    pypi = "devito/devito-4.6.2.tar.gz"

    version("4.6.2", sha256="39c2210a192ad69953b4f8d93440ffd72b07d739c4fe2290e2b182adfb7e143f")

    variant("mpi", default=False, description="Enable MPI support")
    variant("matplotlib", default=False, description="Enable matplolib support")
    variant("ipyparallel", default=False, description="Enable ipyparallel support")
    variant("pandas", default=False, description="Enable pandas support")

    depends_on("py-pip@9.0.1:", type="build")
    depends_on("py-setuptools", type="build")

    depends_on("py-numpy@1.16:", type=("build", "run"))
    depends_on("py-sympy@1.7:1.9", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-flake8@2.1.0:", type=("build", "run"))
    depends_on("py-nbval", type=("build", "run"))
    depends_on("py-cached-property", type=("build", "run"))
    depends_on("py-psutil@5.1.0:5", type=("build", "run"))
    depends_on("py-py-cpuinfo@:8", type=("build", "run"))
    depends_on("py-cgen@2020.1:", type=("build", "run"))
    depends_on("py-codepy@2019.1:", type=("build", "run"))
    depends_on("py-click@:8", type=("build", "run"))
    depends_on("py-codecov", type=("build", "run"))
    depends_on("py-multidict", type=("build", "run"))
    depends_on("py-anytree@2.4.3:2.8", type=("build", "run"))
    depends_on("py-pyrevolve@2.1.3:", type=("build", "run"))
    depends_on("py-distributed@:2022.2", type=("build", "run"))
    depends_on("py-pytest@3.6:6", type=("build", "run"))
    depends_on("py-pytest-runner", type=("build", "run"))
    depends_on("py-pytest-cov", type=("build", "run"))

    # requirements-mpi.tct
    depends_on("py-mpi4py", type=("build", "run"), when="+mpi")

    # requirements-optional.txt
    depends_on("py-matplotlib", type=("build", "run"), when="+matplotlib")
    depends_on("py-ipyparallel", type=("build", "run"), when="+ipyparallel")
    depends_on("py-pandas", type=("build", "run"), when="+pandas")

    depends_on("mpi", type=("build", "run"))

    depends_on("intel-parallel-studio", type="run", when="%intel@:2021.1.1")
    depends_on("intel-oneapi-compilers", type="run", when="%intel@2021.1.2:")

    @run_before("install")
    def add_examples_dir(self):
        # Add file `__init__py` to examples/ so it is picked up by setuptools
        touch("examples/__init__.py")

    def setup_run_environment(self, env):
        # Make benchmark.py available
        env.prepend_path("DEVITO_HOME", self.prefix)

# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
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
    pypi = "devito/devito-4.8.1.tar.gz"

    license("MIT")

    version(
        "4.8.1",
        sha256="f6463354e9be74e54a00e6e522fbb888026df0c04ad2d54a1271708efff7271d",
        url="https://pypi.org/packages/af/6e/a6142333210c1a80309d7ff461b0ad122b52220e97f6b9ddcd5cbbb7b7f6/devito-4.8.1-py3-none-any.whl",
    )

    variant("mpi", default=False, description="Enable MPI support")
    variant("optional", default=False, description="Enable matplolib & pandas support")

    with default_args(type="run"):
        depends_on("py-anytree@2.4.3:2.8", when="@4.6.1:4.8.1")
        depends_on("py-cached-property")
        depends_on("py-cgen@2020:")
        depends_on("py-click", when="@4.6.1:")
        depends_on("py-codepy@2019:")
        depends_on("py-distributed@:2023.3", when="@4.8.1")
        depends_on("py-flake8@2.1:", when="@:4.8.1")
        depends_on("py-ipyparallel@:8.5", when="@4.8.1+mpi")
        depends_on("py-mpi4py", when="@4.7:4.8.2+mpi")
        depends_on("py-multidict")
        depends_on("py-nbval", when="@:4.8.1")
        depends_on("py-numpy@1.16.1:")
        depends_on("py-pip@9.0.1:")
        depends_on("py-psutil@5.1:", when="@4.6.1:")
        depends_on("py-py-cpuinfo", when="@4.8:")
        depends_on("py-pyrevolve@2.1.3:", when="@:4.8.1")
        depends_on("py-pytest@7.2:7", when="@4.8.1")
        depends_on("py-pytest-cov", when="@:4.8.1")
        depends_on("py-pytest-runner", when="@:4.8.1")
        depends_on("py-scipy", when="@:4.8.1")
        depends_on("py-sympy@1.9:1.11", when="@4.8:4.8.1")

    # requirements-mpi.txt

    # requirements-optional.txt

    def setup_run_environment(self, env):
        # Make benchmark.py available
        env.prepend_path("DEVITO_HOME", self.prefix)

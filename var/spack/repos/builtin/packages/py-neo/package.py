# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyNeo(PythonPackage):
    """Neo is a package for representing electrophysiology data in Python,
    together with support for reading a wide range of neurophysiology
    file formats"""

    homepage = "https://neuralensemble.org/neo"
    pypi = "neo/neo-0.4.1.tar.gz"

    version("0.10.2", sha256="2d4218b0826daeea880e155227060029ec38a00238ceb5f097138d9467c6399b")
    version("0.10.0", sha256="e591a53e18cfa4478603a0e133f3fa0e07bc016b2a279d21d72cf8196eca8353")
    version("0.9.0", sha256="6e31c88d7c52174fa2512df589b2b5003e9471fde27fca9f315f4770ba3bd3cb")
    version("0.8.0", sha256="3382a37b24a384006238b72981f1e9259de9bfa71886f8ed564d35d254ace458")
    version("0.5.2", sha256="1de436b7d5e72a5b4f1baa68bae5b790624a9ac44b2673811cb0b6ef554d3f8b")
    version("0.4.1", sha256="a5a4f3aa31654d52789f679717c9fb622ad4f59b56d227dca490357b9de0a1ce")
    version("0.3.3", sha256="6b80eb5bdc9eb4eca829f7464f861c5f1a3a6289559de037930d529bb3dddefb")

    depends_on("py-setuptools", type="build")

    depends_on("py-numpy@1.3.0:", type=("build", "run"), when="@0.3.3:0.4.1")
    depends_on("py-numpy@1.7.1:", type=("build", "run"), when="@0.5.2:0.8.0")
    depends_on("py-numpy@1.13.0:", type=("build", "run"), when="@0.9.0")
    depends_on("py-numpy@1.16.1:", type=("build", "run"), when="@0.10.0:")

    depends_on("py-quantities@0.9.0:", type=("build", "run"), when="@0.3.3:0.8.0")
    depends_on("py-quantities@0.12.1:", type=("build", "run"), when="@0.9.0:")

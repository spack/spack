# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import os

from spack.package import *


class PyTox(PythonPackage):
    """tox is a generic virtualenv management and test command line tool."""

    homepage = "https://tox.readthedocs.org/"
    pypi = "tox/tox-3.14.2.tar.gz"

    version("3.25.0", sha256="37888f3092aa4e9f835fc8cc6dadbaaa0782651c41ef359e3a5743fcb0308160")
    version("3.24.2", sha256="ae442d4d51d5a3afb3711e4c7d94f5ca8461afd27c53f5dd994aba34896cf02d")
    version("3.23.0", sha256="05a4dbd5e4d3d8269b72b55600f0b0303e2eb47ad5c6fe76d3576f4c58d93661")

    depends_on("python@2.7:2.8,3.5:", type=("build", "run"))
    depends_on("py-setuptools", type=("build", "run"))
    depends_on("py-importlib-metadata@1.1.0:", when="^python@:3.7", type=("build", "run"))
    depends_on("py-packaging@14:", type=("build", "run"))
    depends_on("py-pluggy@0.12.0:0", type=("build", "run"))
    depends_on("py-py@1.4.17:1", type=("build", "run"))
    depends_on("py-six@1.0.0:1", type=("build", "run"))
    depends_on("py-virtualenv@16.0.0:", type=("build", "run"))
    depends_on("py-toml@0.9.4:", type=("build", "run"))
    depends_on("py-filelock@3.0.0:3", type=("build", "run"))

    def setup_dependent_package(self, module, dependent_spec):
        tox_path = os.path.join(self.prefix.bin, "tox")
        if os.path.exists(tox_path):
            setattr(module, "tox", Executable(tox_path))

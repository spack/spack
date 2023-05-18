# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyChex(PythonPackage):
    """Chex is a library of utilities for helping to write reliable JAX code."""

    homepage = "https://github.com/deepmind/chex"
    pypi = "chex/chex-0.1.0.tar.gz"

    version("0.1.0", sha256="9e032058f5fed2fc1d5e9bf8e12ece5910cf6a478c12d402b6d30984695f2161")

    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-absl-py@0.9.0:", type=("build", "run"))
    depends_on("py-dm-tree@0.1.5:", type=("build", "run"))
    depends_on("py-jax@0.1.55:", type=("build", "run"))
    depends_on("py-jaxlib@0.1.37:", type=("build", "run"))
    depends_on("py-numpy@1.18.0:", type=("build", "run"))
    depends_on("py-toolz@0.9.0:", type=("build", "run"))

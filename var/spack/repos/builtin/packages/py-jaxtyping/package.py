# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyJaxtyping(PythonPackage):
    """Type annotations and runtime checking for shape and dtype of JAX arrays, and PyTrees."""

    homepage = "https://docs.kidger.site/jaxtyping/"
    pypi = "jaxtyping/jaxtyping-0.2.33.tar.gz"

    license("Apache-2.0")

    version("0.2.33", sha256="9a9cfccae4fe05114b9fb27a5ea5440be4971a5a075bbd0526f6dd7d2730f83e")

    depends_on("python@3.9:", type=("build", "run"))
    depends_on("py-hatchling", type="build")
    depends_on("py-typeguard@2.13.3", type=("build", "run"))

# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTreeMath(PythonPackage):
    """Mathematical operations for JAX pytrees."""

    homepage = "https://github.com/google/tree-math"
    pypi = "tree-math/tree-math-0.2.0.tar.gz"

    license("Apache-2.0")

    version(
        "0.2.0",
        sha256="653e504b77d736ec837f1f418362e4fc37a0dd39478c817cac786536de84cf0c",
        url="https://pypi.org/packages/4b/71/c41359212464e1c2ba55118b4bf530a7b1dcc2731d67391e118c8e26e559/tree_math-0.2.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-jax")

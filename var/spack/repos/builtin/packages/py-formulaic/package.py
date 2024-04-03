# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFormulaic(PythonPackage):
    """Formulaic is a high-performance implementation of Wilkinson formulas
    for Python."""

    homepage = "https://github.com/matthewwardrop/formulaic"
    pypi = "formulaic/formulaic-0.2.4.tar.gz"

    version(
        "0.6.1",
        sha256="3eebbee86bfde23f66c7b86f727b52e4f2af1b08be9ea752d2ea3fe2ff951fe8",
        url="https://pypi.org/packages/ad/79/1ce60c6368cfbfbc186f8ccd45edaa945e0a8dba77469c7f3f0cc44db40e/formulaic-0.6.1-py3-none-any.whl",
    )
    version(
        "0.5.2",
        sha256="65d04b1249584504912eb64f83b47fc1e7e95b0ff3e24fb0859148e2f2f033c2",
        url="https://pypi.org/packages/15/3c/5853059034a58de0b79de67584a22d6fa8f732a1cb7a388942c735584c3e/formulaic-0.5.2-py3-none-any.whl",
    )
    version(
        "0.2.4",
        sha256="775620d93f24f01b33a17aa2cf65a04112003c5112f12015368e4e4605a5013b",
        url="https://pypi.org/packages/45/40/3c337ed87b8ffeb129f21db97bce3d4f1e9125ed4697969348bb6f871931/formulaic-0.2.4-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:", when="@0.3:0.3.2,0.5:")
        depends_on("py-astor@0.8:", when="@0.3.4:0")
        depends_on("py-astor", when="@0.1:0.2")
        depends_on("py-cached-property@1.3:", when="@0.4: ^python@:3.7")
        depends_on("py-graphlib-backport", when="@0.5: ^python@:3.8")
        depends_on("py-interface-meta@1.2:", when="@0.2:0.3.2,0.5:")
        depends_on("py-numpy@1.16.5:", when="@0.5:")
        depends_on("py-numpy", when="@0.2")
        depends_on("py-pandas@1.0.0:", when="@0.4:")
        depends_on("py-pandas", when="@0.1:0.2")
        depends_on("py-scipy@1.6.0:", when="@0.3:")
        depends_on("py-scipy", when="@0.1:0.2")
        depends_on("py-typing-extensions@4.2:", when="@0.5:")
        depends_on("py-wrapt", when="@0.1:")

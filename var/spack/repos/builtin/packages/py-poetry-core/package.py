# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPoetryCore(PythonPackage):
    """Poetry PEP 517 Build Backend."""

    homepage = "https://github.com/python-poetry/poetry-core"
    pypi = "poetry-core/poetry_core-1.6.1.tar.gz"

    license("MIT")

    version(
        "1.8.1",
        sha256="194832b24f3283e01c5402eae71a6aae850ecdfe53f50a979c76bf7aa5010ffa",
        url="https://pypi.org/packages/99/bc/058b8ff87871fce6615ad032d62c773272f243266b110f7b86d146cf78d8/poetry_core-1.8.1-py3-none-any.whl",
    )
    version(
        "1.7.0",
        sha256="38e174cdb00a84ee4a1cab66a378b435747f72414f5573bc18cfc3850a94df38",
        url="https://pypi.org/packages/bf/d4/ce72ac247f414d15ff046f0926b76eb42bd743e83c1df28e856f328e3db1/poetry_core-1.7.0-py3-none-any.whl",
    )
    version(
        "1.6.1",
        sha256="70707340447dee0e7f334f9495ae652481c67b32d8d218f296a376ac2ed73573",
        url="https://pypi.org/packages/fc/7d/e1fb5889102e49e7ef7192f155e9409233255ed64594827b81d4e5950335/poetry_core-1.6.1-py3-none-any.whl",
    )
    version(
        "1.2.0",
        sha256="e248d36c1314dd60fbc66390791923ad8b58c629d3e587080b7c1537a1c0d30f",
        url="https://pypi.org/packages/28/60/6e60b418132aef03e4142064242c4d1e56e96c56979488ed4fc0ba7627c3/poetry_core-1.2.0-py3-none-any.whl",
    )
    version(
        "1.1.0",
        sha256="da16a12054bf3f1ff8656d4c289f99c3d6b7704d272fb174004c4dc82e045954",
        url="https://pypi.org/packages/fa/1a/928afa4256942608bd4a4d4ed4452ce12de1b4e6e4a36b7e67c73cb1b82c/poetry_core-1.1.0-py3-none-any.whl",
    )
    version(
        "1.0.8",
        sha256="54b0fab6f7b313886e547a52f8bf52b8cf43e65b2633c65117f8755289061924",
        url="https://pypi.org/packages/d2/04/08841501db81bceb7a86a98dea7c12b0185fcc69bfdf1aea266f727d1d7e/poetry_core-1.0.8-py2.py3-none-any.whl",
    )
    version(
        "1.0.7",
        sha256="4f8a7f5390d772f42c4c4c3f188e6424b802cb4b57466c6633a1b9ac36f18a43",
        url="https://pypi.org/packages/09/79/5ab16fbf2d9354c242e9f9e784d604dd06842405f7797e71238f3c053200/poetry_core-1.0.7-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.8:3", when="@1.7:")
        depends_on("python@3.7:3", when="@1.1.0-alpha7:1.6")
        depends_on("py-importlib-metadata@1.7:", when="@1.1.0-alpha3:1.6 ^python@:3.7")
        depends_on("py-importlib-metadata@1.7:1", when="@:1.1.0-alpha2 ^python@:3.7")

    # https://github.com/python-poetry/poetry/issues/5547

    def setup_dependent_build_environment(self, env, dependent_spec):
        env.set("GIT_DIR", join_path(dependent_spec.package.stage.source_path, ".git"))

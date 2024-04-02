# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPoetryPluginExport(PythonPackage):
    """Poetry plugin to export the dependencies to various formats"""

    homepage = "https://python-poetry.org/"
    pypi = "poetry-plugin-export/poetry_plugin_export-1.6.0.tar.gz"

    license("MIT")

    version(
        "1.6.0",
        sha256="2dce6204c9318f1f6509a11a03921fb3f461b201840b59f1c237b6ab454dabcf",
        url="https://pypi.org/packages/17/bb/78d7d920bb463e4bee64f44d8b0d4a286a80af7e76ff8326e5169103f44b/poetry_plugin_export-1.6.0-py3-none-any.whl",
    )
    version(
        "1.0.7",
        sha256="dd9d4552e7113a86c97908c13b9a439cb46830f247c7e4969e46a0d8d70e4d3f",
        url="https://pypi.org/packages/07/79/6875ad552af0f2bb98b60fcd281d17620f5ee49f652e34c54969596f780a/poetry_plugin_export-1.0.7-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.8:3", when="@1.5:")
        depends_on("python@3.7:3", when="@:1.4")
        depends_on("py-poetry@1.6:", when="@1.6")
        depends_on("py-poetry@1.2.0:", when="@1.0.7:1.1")
        depends_on("py-poetry-core@1.7:", when="@1.6:")
        depends_on("py-poetry-core@1.1.0:", when="@1.0.7:1.1")

    # depends_on("py-poetry@1.6:1", when="@1.6", type=("build", "run")) # circular dependency
    # depends_on("py-poetry@1.2:1", type="run") # circular dependency

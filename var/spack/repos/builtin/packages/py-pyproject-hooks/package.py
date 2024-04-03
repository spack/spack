# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyprojectHooks(PythonPackage):
    """Wrappers to call pyproject.toml-based build backend hooks."""

    homepage = "https://github.com/pypa/pyproject-hooks"
    pypi = "pyproject_hooks/pyproject_hooks-1.0.0.tar.gz"

    license("MIT")

    version(
        "1.0.0",
        sha256="283c11acd6b928d2f6a7c73fa0d01cb2bdc5f07c57a2eeb6e83d5e56b97976f8",
        url="https://pypi.org/packages/d5/ea/9ae603de7fbb3df820b23a70f6aff92bf8c7770043254ad8d2dc9d6bcba4/pyproject_hooks-1.0.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:")
        depends_on("py-tomli@1.1:", when="@1: ^python@:3.10")

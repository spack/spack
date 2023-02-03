# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyprojectHooks(Package, PythonExtension):
    """Wrappers to call pyproject.toml-based build backend hooks."""

    homepage = "https://github.com/pypa/pyproject-hooks"
    # Must be installed from wheel to avoid circular dependency on build
    url = "https://files.pythonhosted.org/packages/py3/p/pyproject_hooks/pyproject_hooks-1.0.0-py3-none-any.whl"
    list_url = "https://pypi.org/simple/pyproject_hooks/"

    version("1.0.0", sha256="283c11acd6b928d2f6a7c73fa0d01cb2bdc5f07c57a2eeb6e83d5e56b97976f8", expand=False)

    extends("python")
    depends_on("py-installer", type="build")

    depends_on("py-tomli@1.1:", when="^python@:3.10", type=("build", "run"))

    def install(self, spec, prefix):
        installer("--prefix", prefix, self.stage.archive_file)

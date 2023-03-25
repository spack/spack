# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyprojectHooks(PythonPackage):
    """Wrappers to call pyproject.toml-based build backend hooks."""

    homepage = "https://github.com/pypa/pyproject-hooks"
    url = "https://github.com/pypa/pyproject-hooks/archive/refs/tags/v1.0.0.tar.gz"
    list_url = "https://github.com/pypa/pyproject-hooks/tags/"

    version("1.0.0", sha256="d45c52f9af6bce94755eecf9dbfe6b3c89ef9a50088a8809f5bbec4ed0f9be0b")

    depends_on("py-flit-core@3.2:3", type="build")
    depends_on("py-tomli@1.1:", when="^python@:3.10", type=("build", "run"))

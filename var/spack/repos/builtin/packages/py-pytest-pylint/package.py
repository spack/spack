# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPytestPylint(PythonPackage):
    """Run pylint with pytest and have configurable rule types (i.e.
    Convention, Warn, and Error) fail the build. You can also specify a
    pylintrc file.

    """

    homepage = "https://pypi.org/project/pytest-pylint/"
    pypi = "pytest-pylint/pytest-pylint-0.21.0.tar.gz"
    git = "https://github.com/pytest-dev/pytest"

    license("MIT")

    version(
        "0.21.0",
        sha256="f10d9eaa72b9fbe624ee4b55da0481f56482eee0a467afc1ee3ae8b1fefbd0b4",
        url="https://pypi.org/packages/a7/4b/23f6ce5187eec09ae282f91d88f6b9e1d871fc89b839dcfd0b94e4591353/pytest_pylint-0.21.0-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("python@3.7:", when="@0.19:")
        depends_on("py-pylint@2.15:", when="@0.21:")
        depends_on("py-pytest@7.0.0:", when="@0.21:")
        depends_on("py-tomli@1.1:", when="@0.21: ^python@:3.10")

# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.python import PythonPackage

from spack.package import *


class PyWatchfiles(PythonPackage):
    """Simple, modern and high performance file watching and code reload in python."""

    homepage = "https://github.com/samuelcolvin/watchfiles"
    pypi = "watchfiles/watchfiles-0.18.1.tar.gz"

    maintainers("viperML")

    license("MIT")

    version("1.0.5", sha256="b7529b5dcc114679d43827d8c35a07c493ad6f083633d573d81c660abc5979e9")
    version("0.18.1", sha256="4ec0134a5e31797eb3c6c624dbe9354f2a8ee9c720e0b46fc5b7bab472b7c6d4")

    depends_on("py-maturin@0.13", type="build", when="@0.18.1")
    depends_on("py-maturin@0.14:2", type="build", when="@1:")
    depends_on("py-anyio@3:", type=("build", "run"))

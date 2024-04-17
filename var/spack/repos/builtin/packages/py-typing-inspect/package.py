# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTypingInspect(PythonPackage):
    """Runtime inspection utilities for typing module."""

    homepage = "https://github.com/ilevkivskyi/typing_inspect"
    pypi = "typing_inspect/typing_inspect-0.8.0.tar.gz"

    license("MIT")

    version(
        "0.8.0",
        sha256="5fbf9c1e65d4fa01e701fe12a5bca6c6e08a4ffd5bc60bfac028253a447c5188",
        url="https://pypi.org/packages/be/01/59b743dca816c4b6ca891b9e0f84d20513cd61bdbbaa8615de8f5aab68c1/typing_inspect-0.8.0-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("py-mypy-extensions@0.3:", when="@0.3.1:")
        depends_on("py-typing-extensions@3.7.4:", when="@0.5:")

# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTorchdata(PythonPackage):
    """Composable data loading modules for PyTorch."""

    homepage = "https://github.com/pytorch/data"
    git = "https://github.com/pytorch/data.git"
    url = "https://github.com/pytorch/data/archive/refs/tags/v0.4.0.tar.gz"

    maintainers("adamjstewart")

    license("BSD-3-Clause")

    version(
        "0.3.0",
        sha256="bd16fe37cd9a3dc1960503557b5d556251e1f32b9078ed91a27dce518eb328d6",
        url="https://pypi.org/packages/7c/86/fe5c8d7531110d4ac5d314fb58730c4f1b9e8a4dc4729827dd7ee2d7b9a0/torchdata-0.3.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-requests", when="@0.3:")
        depends_on("py-torch@1.11", when="@0.3.0:")
        depends_on("py-urllib3@1.25:", when="@0.3.0:")

    # https://github.com/pytorch/data#version-compatibility

    # pyproject.toml

    # CMakeLists.txt

    # https://github.com/pytorch/data#version-compatibility

    # requirements.txt

    # third_party/CMakeLists.txt

    def setup_build_environment(self, env):
        env.set("USE_SYSTEM_LIBS", "ON")

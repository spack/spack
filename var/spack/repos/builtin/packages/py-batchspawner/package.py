# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBatchspawner(PythonPackage):
    """This is a custom spawner for Jupyterhub that is designed for
    installations on clusters using batch scheduling software."""

    homepage = "https://github.com/jupyterhub/batchspawner"
    pypi = "batchspawner/batchspawner-1.1.0.tar.gz"

    license("BSD-3-Clause")

    version(
        "1.1.0",
        sha256="d7e203128700c9105c660bf139a2dfe132e4c92708292576ea7ffe7985ed1481",
        url="https://pypi.org/packages/27/de/b9f3cf50d90167cca00e2f98f501038e0d2fb9a918343abfb767df000976/batchspawner-1.1.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@:3", when="@:1.2")
        depends_on("py-async-generator@1.8:", when="@1:1.2")
        depends_on("py-jinja2", when="@1:1.2")
        depends_on("py-jupyterhub@0.5:", when="@:1.1")

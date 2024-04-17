# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGradioClient(PythonPackage):
    """Python library for easily interacting with trained machine learning models"""

    homepage = "https://github.com/gradio-app/gradio"
    pypi = "gradio_client/gradio_client-0.2.9.tar.gz"

    version(
        "0.2.9",
        sha256="9174476e8965b6f622a4426d631c1c29f2209329f110242278fcb6ad26f813d5",
        url="https://pypi.org/packages/fc/be/50b4ba7b5ab067e31b67526f9cdbdd2241854af2f6b205f678c9da316ac9/gradio_client-0.2.9-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("python@3.8:", when="@0.2.7:")
        depends_on("py-fsspec")
        depends_on("py-httpx", when="@:0.10.0")
        depends_on("py-huggingface-hub@0.13.0:", when="@:0.7.1")
        depends_on("py-packaging")
        depends_on("py-requests", when="@:0.2.9")
        depends_on("py-typing-extensions", when="@:0.2.9")
        depends_on("py-websockets", when="@:0.2.9")

# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGradio(PythonPackage):
    """Python library for easily interacting with trained machine learning models"""

    homepage = "https://github.com/gradio-app/gradio"
    pypi = "gradio/gradio-3.36.1.tar.gz"

    license("Apache-2.0")

    version(
        "3.36.1",
        sha256="69f60c29d79fb93b2545466d367e5998d6db57379469a4067c8717ccd34015e1",
        url="https://pypi.org/packages/98/ad/be1bdac5810d3b8497a8a1361e922180f43ec8634cca28cc6b5de68cb18d/gradio-3.36.1-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.8:", when="@3.35:")
        depends_on("py-aiofiles", when="@:3.36")
        depends_on("py-aiohttp", when="@:3.36")
        depends_on("py-altair@4.2.0:", when="@:3.36")
        depends_on("py-fastapi")
        depends_on("py-ffmpy")
        depends_on("py-gradio-client@0.2.7:", when="@3.35:3.36")
        depends_on("py-httpx", when="@:4.19.1")
        depends_on("py-huggingface-hub@0.14.0:0.14.0.0,0.14.1:", when="@3.33:4.8")
        depends_on("py-jinja2", when="@:3.36")
        depends_on("py-markdown-it-py@2:+linkify", when="@:3.40")
        depends_on("py-markupsafe", when="@:3.36")
        depends_on("py-matplotlib", when="@:3.36")
        depends_on("py-mdit-py-plugins@:0.3.3", when="@:3.40")
        depends_on("py-numpy", when="@:3.36")
        depends_on("py-orjson", when="@:3.36")
        depends_on("py-pandas", when="@:3.36")
        depends_on("py-pillow", when="@:3.36")
        depends_on("py-pydantic", when="@:3.36")
        depends_on("py-pydub")
        depends_on("py-pygments@2.12:", when="@:3.36")
        depends_on("py-python-multipart", when="@:4.19.0")
        depends_on("py-pyyaml", when="@:3.36")
        depends_on("py-requests", when="@:3.36")
        depends_on("py-semantic-version", when="@:3.36")
        depends_on("py-uvicorn@0.14:")
        depends_on("py-websockets@10:", when="@:3.36")

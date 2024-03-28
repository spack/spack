# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyOpenai(PythonPackage):
    """The OpenAI Python library provides convenient access to the OpenAI API
    from applications written in the Python language. It includes a pre-defined
    set of classes for API resources that initialize themselves dynamically from
    API responses which makes it compatible with a wide range of versions of the
    OpenAI API."""

    homepage = "https://github.com/openai/openai-python"
    pypi = "openai/openai-0.27.8.tar.gz"

    license("MIT")

    version(
        "0.27.8",
        sha256="e0a7c2f7da26bdbe5354b03c6d4b82a2f34bd4458c7a17ae1a7092c3e397e03c",
        url="https://pypi.org/packages/67/78/7588a047e458cb8075a4089d721d7af5e143ff85a2388d4a28c530be0494/openai-0.27.8-py3-none-any.whl",
    )

    variant("datalib", default=False)
    variant("embeddings", default=False)
    variant("wandb", default=False)

    with default_args(type="run"):
        depends_on("py-aiohttp", when="@0.27:0.27.0,0.27.2:0")
        depends_on("py-matplotlib", when="@0.27:0.27.0,0.27.2:0+embeddings")
        depends_on("py-numpy", when="@0.27:0.27.0,0.27.2:0+wandb")
        depends_on("py-numpy", when="@0.27:0.27.0,0.27.2:0+embeddings")
        depends_on("py-numpy", when="@0.27:0.27.0,0.27.2:0+datalib")
        depends_on("py-openpyxl@3.0.7:", when="@0.27:0.27.0,0.27.2:0+wandb")
        depends_on("py-openpyxl@3.0.7:", when="@0.27:0.27.0,0.27.2:0+embeddings")
        depends_on("py-openpyxl@3.0.7:", when="@0.27:0.27.0,0.27.2:0+datalib")
        depends_on("py-pandas@1.2.3:", when="@0.27:0.27.0,0.27.2:+datalib")
        depends_on("py-pandas@1.2.3:", when="@0.27:0.27.0,0.27.2:0+wandb")
        depends_on("py-pandas@1.2.3:", when="@0.27:0.27.0,0.27.2:0+embeddings")
        depends_on("py-pandas-stubs@1.1.0.11:", when="@0.27:0.27.0,0.27.2:+datalib")
        depends_on("py-pandas-stubs@1.1.0.11:", when="@0.27:0.27.0,0.27.2:0+wandb")
        depends_on("py-pandas-stubs@1.1.0.11:", when="@0.27:0.27.0,0.27.2:0+embeddings")
        depends_on("py-plotly", when="@0.27:0.27.0,0.27.2:0+embeddings")
        depends_on("py-requests@2.20:", when="@0.27:0.27.0,0.27.2:0")
        depends_on("py-scikit-learn@1.0.2:", when="@0.27:0.27.0,0.27.2:0+embeddings")
        depends_on("py-scipy", when="@0.27:0.27.0,0.27.2:0+embeddings")
        depends_on("py-tenacity@8.0.1:", when="@0.27:0.27.0,0.27.2:0+embeddings")
        depends_on("py-tqdm", when="@0.27:0.27.0,0.27.2:0")
        depends_on("py-wandb", when="@0.27:0.27.0,0.27.2:0+wandb")

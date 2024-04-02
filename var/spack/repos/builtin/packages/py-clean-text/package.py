# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCleanText(PythonPackage):
    """User-generated content on the Web and in social media is
    often dirty. Preprocess your scraped data with clean-text
    to create a normalized text representation."""

    pypi = "clean-text/clean-text-0.5.0.tar.gz"

    license("Apache-2.0")

    version(
        "0.6.0",
        sha256="4fedb156042f192cdef9ed5324b281465f1116aba96791e9289384a2e6bec4da",
        url="https://pypi.org/packages/34/7f/c99da1cf5b69ed112b3f21029f2cbf37ee4dbffc4607fa0c5601f1991410/clean_text-0.6.0-py3-none-any.whl",
    )
    version(
        "0.5.0",
        sha256="b83f39c72189a6e9c1356e31079cdcedc67d8e31e90cde788e60680ea0704afd",
        url="https://pypi.org/packages/8e/1f/acc62e76dddb52e56d8e6ef20377e3e26976e4ad3ded582b1ff1d18505d7/clean_text-0.5.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:", when="@0.6:")
        depends_on("py-emoji@1", when="@0.6:")
        depends_on("py-emoji", when="@0.3:0.5")
        depends_on("py-ftfy@6:", when="@0.4:")

# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMarkdown2(PythonPackage):
    """A fast and complete Python implementation of Markdown."""

    homepage = "https://github.com/trentm/python-markdown2"
    pypi = "markdown2/markdown2-2.3.9.tar.gz"

    license("MIT")

    version(
        "2.4.0",
        sha256="8d4ef4a2d090c99532069c4611a9a2b9bea6ae1fa29b6c3727c95d1e31a8f6c5",
        url="https://pypi.org/packages/5d/be/3924cc1c0e12030b5225de2b4521f1dc729730773861475de26be64a0d2b/markdown2-2.4.0-py2.py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("python@:3", when="@2.4:")

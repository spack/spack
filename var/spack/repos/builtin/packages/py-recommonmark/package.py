# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyRecommonmark(PythonPackage):
    """A docutils-compatibility bridge to CommonMark.

    This allows you to write CommonMark inside of Docutils & Sphinx projects.

    Documentation is available on Read the Docs:
    http://recommonmark.readthedocs.org"""

    homepage = "https://github.com/readthedocs/recommonmark"
    pypi = "recommonmark/recommonmark-0.6.0.tar.gz"

    license("MIT")

    version(
        "0.6.0",
        sha256="2ec4207a574289355d5b6ae4ae4abb29043346ca12cdd5f07d374dc5987d2852",
        url="https://pypi.org/packages/94/de/334aaf73df8c0e77fb07f883d1e274344526196c137ef3479cb5e5aef086/recommonmark-0.6.0-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-commonmark@0.8.1:", when="@0.6:")
        depends_on("py-docutils@0.11:", when="@0.0.2:0.4,0.6:")
        depends_on("py-sphinx@1.3.1:", when="@0.6:")

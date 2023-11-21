# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyTokenizers(PythonPackage):
    """Fast and Customizable Tokenizers."""

    homepage = "https://github.com/huggingface/tokenizers"
    pypi = "tokenizers/tokenizers-0.6.0.tar.gz"

    version("0.15.0", sha256="10c7e6e7b4cabd757da59e93f5f8d1126291d16f8b54f28510825ef56a3e5d0e")
    version("0.14.1", sha256="ea3b3f8908a9a5b9d6fc632b5f012ece7240031c44c6d4764809f33736534166")
    version("0.13.3", sha256="2e546dbb68b623008a5442353137fbb0123d311a6d7ba52f2667c8862a75af2e")
    version("0.13.1", sha256="3333d1cee5c8f47c96362ea0abc1f81c77c9b92c6c3d11cbf1d01985f0d5cf1d")
    version("0.10.3", sha256="1a5d3b596c6d3a237e1ad7f46c472d467b0246be7fd1a364f12576eb8db8f7e6")
    version("0.6.0", sha256="1da11fbfb4f73be695bed0d655576097d09a137a16dceab2f66399716afaffac")
    version("0.5.2", sha256="b5a235f9c71d04d4925df6c4fa13b13f1d03f9b7ac302b89f8120790c4f742bc")

    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools-rust", type="build")

    # will not build with rust 1.73 until 0.14.1
    # https://github.com/huggingface/tokenizers/issues/1359
    depends_on("py-setuptools-rust^rust@:1.72.1", when="@0.11:0.13", type="build")

    # A nightly or dev version of rust is required to build older versions.
    # https://github.com/huggingface/tokenizers/issues/176
    # https://github.com/PyO3/pyo3/issues/5
    depends_on("rust@nightly", when="@:0.10", type="build")

    # TODO: This package currently requires internet access to install.

    # cargo resolves dependencies, which includes openssl-sys somewhere, which needs
    # system pkgconfig and openssl.
    depends_on("pkgconfig", type="build")
    depends_on("openssl")

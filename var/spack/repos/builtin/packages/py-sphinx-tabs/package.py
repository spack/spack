# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PySphinxTabs(PythonPackage):
    """Create tabbed content in Sphinx documentation when building HTML."""

    homepage = "https://github.com/executablebooks/sphinx-tabs"
    pypi = "sphinx-tabs/sphinx-tabs-3.2.0.tar.gz"

    maintainers("schmitts")

    license("MIT")

    version(
        "3.4.4",
        sha256="85939b689a0b0a24bf0da418b9acf14b0b0fca7a7a5cd35461ee452a2d4e716b",
        url="https://pypi.org/packages/ff/a0/82125f3a296bece2ac4673f4b4dc676049c2dc87344b14aa65341f6c950b/sphinx_tabs-3.4.4-py3-none-any.whl",
    )
    version(
        "3.4.1",
        sha256="7cea8942aeccc5d01a995789c01804b787334b55927f29b36ba16ed1e7cb27c6",
        url="https://pypi.org/packages/4f/2d/80293fbb2aa82d457f9df0de85800b11e3bfd5008b118bddb303a797e5c5/sphinx_tabs-3.4.1-py3-none-any.whl",
    )
    version(
        "3.3.1",
        sha256="73209aa769246501f6de9e33051cfd2d54f5900e0cc28a63367d8e4af4c0db5d",
        url="https://pypi.org/packages/a5/d7/beda6ab57bb591416f95dfb2486960a7f4f4db43105993a5b02c4782803b/sphinx_tabs-3.3.1-py3-none-any.whl",
    )
    version(
        "3.2.0",
        sha256="1e1b1846c80137bd81a78e4a69b02664b98b1e1da361beb30600b939dfc75065",
        url="https://pypi.org/packages/15/be/4fa8ecfb7a9ba5e8d5aa6e27351faaf5f20c9066652064e473a853431916/sphinx_tabs-3.2.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:3", when="@3.4:")
        depends_on("python@:3", when="@1.2:3.3")
        depends_on("py-docutils@0.18", when="@3.4.1:3.4.4")
        depends_on("py-docutils@0.17", when="@3.3:3.4.0")
        depends_on("py-docutils@0.16", when="@3:3.2")
        depends_on("py-pygments", when="@1.2:")
        depends_on("py-sphinx", when="@3.4.1:")
        depends_on("py-sphinx@2.0.0:4", when="@3:3.3")

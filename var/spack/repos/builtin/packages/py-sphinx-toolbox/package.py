# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySphinxToolbox(PythonPackage):
    """Box of handy tools for Sphinx."""

    homepage = "https://github.com/sphinx-toolbox/sphinx-toolbox"
    pypi = "sphinx_toolbox/sphinx_toolbox-3.4.0.tar.gz"

    maintainers("LydDeb")

    version(
        "3.4.0",
        sha256="cdf70facee515a2d9406d568a253fa3e89f930fde23c4e8095ba0c675f7c0a48",
        url="https://pypi.org/packages/63/ba/7eb6695cf42038545be89f839de5ffd06d1de7197f0f5a58544facdb87eb/sphinx_toolbox-3.4.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-apeye@0.4:", when="@2.15.3:")
        depends_on("py-autodocsumm@0.2:", when="@0.7:2.10,2.15:")
        depends_on("py-beautifulsoup4@4.9.1:", when="@0.1.1:")
        depends_on("py-cachecontrol@0.12.6:+filecache", when="@2.11.1,2.15.3:3.4")
        depends_on("py-dict2css@0.2.3:", when="@2.13:")
        depends_on("py-docutils@0.16:0.18", when="@3.2:3.4")
        depends_on("py-domdf-python-tools@2.9:", when="@2.11.2:")
        depends_on("py-html5lib@1.1:", when="@0.1.1:")
        depends_on("py-lockfile@0.12:", when="@2.15.3:3.4")
        depends_on("py-ruamel-yaml@0.16.12:", when="@1.6:")
        depends_on("py-sphinx@3.2:", when="@1.8.1:1.8.2,2.16.1:")
        depends_on("py-sphinx-autodoc-typehints@1.11.1:", when="@3.1:")
        depends_on("py-sphinx-jinja2-compat", when="@2.18.1:")
        depends_on("py-sphinx-prompt@1.1:", when="@0.3:")
        depends_on("py-sphinx-tabs@1.2.1:", when="@3.1.2:")
        depends_on("py-tabulate@0.8.7:", when="@1.6:")
        depends_on("py-typing-extensions@3.7.4.3:3.10.0.0,3.10.0.2:", when="@2.14:")

# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySphinxRtdTheme(PythonPackage):
    """ReadTheDocs.org theme for Sphinx."""

    homepage = "https://github.com/readthedocs/sphinx_rtd_theme"
    pypi = "sphinx-rtd-theme/sphinx_rtd_theme-0.5.1.tar.gz"

    license("MIT")

    version(
        "1.2.2",
        sha256="6a7e7d8af34eb8fc57d52a09c6b6b9c46ff44aea5951bc831eeb9245378f3689",
        url="https://pypi.org/packages/85/32/9ccebf3a82c085e8fc12b67cc3dbf840789fb6c7835ed0d61686d6509aa9/sphinx_rtd_theme-1.2.2-py2.py3-none-any.whl",
    )
    version(
        "1.2.0",
        sha256="f823f7e71890abe0ac6aaa6013361ea2696fc8d3e1fa798f463e82bdb77eeff2",
        url="https://pypi.org/packages/b3/46/c167351699e5dc126798385cf37c26ba9df7a26c6f8855661d9f966d6ced/sphinx_rtd_theme-1.2.0-py2.py3-none-any.whl",
    )
    version(
        "1.0.0",
        sha256="4d35a56f4508cfee4c4fb604373ede6feae2a306731d533f409ef5c3496fdbd8",
        url="https://pypi.org/packages/e0/d2/3818e4730e314719e27f639c44164419e40eed826d63753dc480262036e8/sphinx_rtd_theme-1.0.0-py2.py3-none-any.whl",
    )
    version(
        "0.5.2",
        sha256="4a05bdbe8b1446d77a01e20a23ebc6777c74f43237035e76be89699308987d6f",
        url="https://pypi.org/packages/ac/24/2475e8f83519b54b2148d4a56eb1111f9cec630d088c3ffc214492c12107/sphinx_rtd_theme-0.5.2-py2.py3-none-any.whl",
    )
    version(
        "0.5.1",
        sha256="fa6bebd5ab9a73da8e102509a86f3fcc36dec04a0b52ea80e5a033b2aba00113",
        url="https://pypi.org/packages/76/81/d5af3a50a45ee4311ac2dac5b599d69f68388401c7a4ca902e0e450a9f94/sphinx_rtd_theme-0.5.1-py2.py3-none-any.whl",
    )
    version(
        "0.5.0",
        sha256="373413d0f82425aaa28fb288009bf0d0964711d347763af2f1b65cafcb028c82",
        url="https://pypi.org/packages/c3/86/1addf25a238bbd8466bb099f23d9a9f13494b22b37b44f6c41a778b8730f/sphinx_rtd_theme-0.5.0-py2.py3-none-any.whl",
    )
    version(
        "0.4.3",
        sha256="00cf895504a7895ee433807c62094cf1e95f065843bf3acd17037c3e9a2becd4",
        url="https://pypi.org/packages/60/b4/4df37087a1d36755e3a3bfd2a30263f358d2dea21938240fa02313d45f51/sphinx_rtd_theme-0.4.3-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-docutils@:0.18", when="@1.2:2.0.0-rc1")
        depends_on("py-docutils@:0.17", when="@1:1.1")
        depends_on("py-docutils@:0.16", when="@0.5.2:0")
        depends_on("py-sphinx@1.6.1:6", when="@1.2.0-rc2:1.2")
        depends_on("py-sphinx@1.6.1:", when="@1:1.0")
        depends_on("py-sphinx", when="@0.4.1:0")
        depends_on("py-sphinxcontrib-jquery@4:", when="@1.2.2-rc1:")
        depends_on("py-sphinxcontrib-jquery@2,4:", when="@1.2.0-rc4:1.2.1")

    conflicts("^py-sphinxcontrib-jquery@3.0.0")

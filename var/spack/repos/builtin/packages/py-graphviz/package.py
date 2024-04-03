# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyGraphviz(PythonPackage):
    """Simple Python interface for Graphviz"""

    homepage = "https://github.com/xflr6/graphviz"
    pypi = "graphviz/graphviz-0.10.1.zip"

    license("MIT")

    version(
        "0.13.2",
        sha256="241fb099e32b8e8c2acca747211c8237e40c0b89f24b1622860075d59f4c4b25",
        url="https://pypi.org/packages/f5/74/dbed754c0abd63768d3a7a7b472da35b08ac442cf87d73d5850a6f32391e/graphviz-0.13.2-py2.py3-none-any.whl",
    )
    version(
        "0.13",
        sha256="df54c2e0d2c8df6aee3397eb44de186d94e2a0610f4052649bfbb26d03d56850",
        url="https://pypi.org/packages/94/cd/7b37f2b658995033879719e1ea4c9f171bf7a14c16b79220bd19f9eda3fe/graphviz-0.13-py2.py3-none-any.whl",
    )
    version(
        "0.12",
        sha256="8adc6460f9eddca440b826dd89790090d76fb8e693e2206fd4c2a4ed80841999",
        url="https://pypi.org/packages/17/51/d6de512dbbbab95f0adb53fb2a4396b79722f7c3fbe8ecc2d8c6ab7de00a/graphviz-0.12-py2.py3-none-any.whl",
    )
    version(
        "0.11.1",
        sha256="6d0f69c107cfdc9bd1df3763fad99569bbcba29d0c52ffcbc6f266621d8bf709",
        url="https://pypi.org/packages/5c/b1/016e657586843f40b4daa66127ce1ee9e3285ff15baf5d80946644a98aeb/graphviz-0.11.1-py2.py3-none-any.whl",
    )
    version(
        "0.10.1",
        sha256="0e1744a45b0d707bc44f99c7b8e5f25dc22cf96b6aaf2432ac308ed9822a9cb6",
        url="https://pypi.org/packages/1f/e2/ef2581b5b86625657afd32030f90cf2717456c1d2b711ba074bf007c0f1a/graphviz-0.10.1-py2.py3-none-any.whl",
    )
    version(
        "0.8.4",
        sha256="7caa53f0b0be42c5f2eaa3f3d71dcc863b15bacceb5d531c2ad7519e1980ff82",
        url="https://pypi.org/packages/53/39/4ab213673844e0c004bed8a0781a0721a3f6bb23eb8854ee75c236428892/graphviz-0.8.4-py2.py3-none-any.whl",
    )

    variant("dev", default=False, description="development mode")
    variant("docs", default=False, description="build documentation")

    with default_args(type="run"):
        depends_on("py-flake8", when="@0.8.2:+dev")
        depends_on("py-pep8-naming", when="@0.8.2:+dev")
        depends_on("py-sphinx@1.7.0:", when="@0.10:0.14.0+docs")
        depends_on("py-sphinx@1.3:", when="@0.8.3:0.9+docs")
        depends_on("py-sphinx-rtd-theme", when="@0.8.3:+docs")
        depends_on("py-tox@3.0.0:", when="@0.8.3:+dev")
        depends_on("py-twine", when="@0.8.2:+dev")
        depends_on("py-wheel", when="@0.8.2:+dev")

# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFlitCore(Package, PythonExtension):
    """Distribution-building parts of Flit."""

    homepage = "https://github.com/takluyver/flit"
    # Must be installed from wheel to avoid circular dependency on build
    url = (
        "https://files.pythonhosted.org/packages/py3/f/flit-core/flit_core-3.8.0-py3-none-any.whl"
    )
    list_url = "https://pypi.org/simple/flit-core/"

    maintainers("takluyver")

    version(
        "3.8.0",
        sha256="64a29ec845164a6abe1136bf4bc5ae012bdfe758ed42fc7571a9059a7c80bd83",
        expand=False,
    )
    version(
        "3.7.1",
        sha256="e454fdbf68c7036e1c7435ec7479383f9d9a1650ca5b304feb184eba1efcdcef",
        expand=False,
    )
    version(
        "3.6.0",
        sha256="7661029dedadd456c1d94e0a4765222447f00808bb1fcc767e4270a883ba8b4c",
        expand=False,
    )
    version(
        "3.5.1",
        sha256="42d144fa25df9493bfb655036279c4a4ed323e2e3db178b757e898af5aba0334",
        expand=False,
    )
    version(
        "3.5.0",
        sha256="81f0b35a7abedeb2233c66cd801d07130593c272efbbe789634f6a680946a6f0",
        expand=False,
    )
    version(
        "3.4.0",
        sha256="dcd076725ea009ff4b4db65f173ffa9fadb07e736601a4773f1c6b6fcf5f4b0e",
        expand=False,
    )
    version(
        "3.3.0",
        sha256="9b247b3095cb3c43933a59a7433f92ddfdd7fc843e08ef0f4550d53a9cfbbef6",
        expand=False,
    )
    version(
        "3.2.0",
        sha256="6f25843e908dfc3e907b6b9ee71e3d185bcb5aebab8c3431e4e34c261e5ff1b5",
        expand=False,
    )
    version(
        "3.1.0",
        sha256="1d06e64a6af7e1fd1496563b160df29dd32714e00b473f3b763f6e6810476517",
        expand=False,
    )
    version(
        "3.0.0",
        sha256="a787754978cfe3c192a5fc6baf2179ae85b05395804de7d7fe2864d9431e8d03",
        expand=False,
    )
    version(
        "2.3.0",
        sha256="a8f8904b534966712390e0a2e434cd33f76037730a0aaed299a286f9e18cac2b",
        expand=False,
    )

    extends("python")
    depends_on("py-installer", type="build")

    # flit_core/build_thyself.py
    depends_on("py-tomli", when="@3.4:3.5", type=("build", "run"))
    depends_on("py-toml", when="@3.1:3.3", type=("build", "run"))
    depends_on("py-pytoml", when="@:3.0", type=("build", "run"))

    def url_for_version(self, version):
        url = "https://files.pythonhosted.org/packages/{0}/f/flit-core/flit_core-{1}-{0}-none-any.whl"
        if version >= Version("3"):
            language = "py3"
        else:
            language = "py2.py3"
        return url.format(language, version)

    def install(self, spec, prefix):
        installer("--prefix", prefix, self.stage.archive_file)

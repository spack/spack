# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFlitCore(PythonPackage):
    """Distribution-building parts of Flit."""

    homepage = "https://github.com/pypa/flit"
    pypi = "flit-core/flit_core-3.9.0.tar.gz"

    # Tests import of a non-existing package
    skip_modules = ["flit_core.tests"]
    tags = ["build-tools"]

    maintainers("takluyver")

    license("BSD-3-Clause")

    version(
        "3.9.0",
        sha256="7aada352fb0c7f5538c4fafeddf314d3a6a92ee8e2b1de70482329e42de70301",
        url="https://pypi.org/packages/38/45/618e84e49a6c51e5dd15565ec2fcd82ab273434f236b8f108f065ded517a/flit_core-3.9.0-py3-none-any.whl",
    )
    version(
        "3.8.0",
        sha256="64a29ec845164a6abe1136bf4bc5ae012bdfe758ed42fc7571a9059a7c80bd83",
        url="https://pypi.org/packages/04/ac/f91a0219e0d4162762f218e4876bf328f16e4d283e691cd7f42a02b22634/flit_core-3.8.0-py3-none-any.whl",
    )
    version(
        "3.7.1",
        sha256="e454fdbf68c7036e1c7435ec7479383f9d9a1650ca5b304feb184eba1efcdcef",
        url="https://pypi.org/packages/ad/38/80992c4cb490a05474c886850ec818276d09c0a6722bd5b43bc487818ac7/flit_core-3.7.1-py3-none-any.whl",
    )
    version(
        "3.6.0",
        sha256="7661029dedadd456c1d94e0a4765222447f00808bb1fcc767e4270a883ba8b4c",
        url="https://pypi.org/packages/c8/e8/920a6b202831b9d0e21113dd5b7e78d094ca830c9dc4404e70367ff8b2eb/flit_core-3.6.0-py3-none-any.whl",
    )
    version(
        "3.5.1",
        sha256="42d144fa25df9493bfb655036279c4a4ed323e2e3db178b757e898af5aba0334",
        url="https://pypi.org/packages/32/56/f3e180eea51e3e085b1da06233f6e6aa9adb04000d19ba91c29e44823bf7/flit_core-3.5.1-py3-none-any.whl",
    )
    version(
        "3.5.0",
        sha256="81f0b35a7abedeb2233c66cd801d07130593c272efbbe789634f6a680946a6f0",
        url="https://pypi.org/packages/16/d6/5db8ba55264d8cc61a101e04e6e329650874e046b102ed09970bb0502437/flit_core-3.5.0-py3-none-any.whl",
    )
    version(
        "3.4.0",
        sha256="dcd076725ea009ff4b4db65f173ffa9fadb07e736601a4773f1c6b6fcf5f4b0e",
        url="https://pypi.org/packages/16/3a/4e107184bbaff2f84d37813bc31f5e0499afa7b1db23419dee95640fc076/flit_core-3.4.0-py3-none-any.whl",
    )
    version(
        "3.3.0",
        sha256="9b247b3095cb3c43933a59a7433f92ddfdd7fc843e08ef0f4550d53a9cfbbef6",
        url="https://pypi.org/packages/87/5e/b4d6334fd01716e08a76204ffd85031b640567b7548ac79f258f40eded6b/flit_core-3.3.0-py3-none-any.whl",
    )
    version(
        "3.2.0",
        sha256="6f25843e908dfc3e907b6b9ee71e3d185bcb5aebab8c3431e4e34c261e5ff1b5",
        url="https://pypi.org/packages/67/f6/382ac797101385edb1908e1105121ac33f910cd06d126ac9ac1bd540a3b3/flit_core-3.2.0-py3-none-any.whl",
    )
    version(
        "3.1.0",
        sha256="1d06e64a6af7e1fd1496563b160df29dd32714e00b473f3b763f6e6810476517",
        url="https://pypi.org/packages/ed/0c/50352b127c0936cd59dd762db41d0e17986401c42ba613fa502e926d33ec/flit_core-3.1.0-py3-none-any.whl",
    )
    version(
        "3.0.0",
        sha256="a787754978cfe3c192a5fc6baf2179ae85b05395804de7d7fe2864d9431e8d03",
        url="https://pypi.org/packages/a8/66/67758f788959c2557c4d0f80e4895c3c0802873be95b82a5213ea39542d7/flit_core-3.0.0-py3-none-any.whl",
    )
    version(
        "2.3.0",
        sha256="a8f8904b534966712390e0a2e434cd33f76037730a0aaed299a286f9e18cac2b",
        url="https://pypi.org/packages/4b/3c/82798771fc1fd978c9225c5ae25eef45cb23b0df4728f208024a5b57901f/flit_core-2.3.0-py2.py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("py-pytoml", when="@2.0-rc2:3.0")
        depends_on("py-toml", when="@3.1:3.3")
        depends_on("py-tomli", when="@3.4:3.5")

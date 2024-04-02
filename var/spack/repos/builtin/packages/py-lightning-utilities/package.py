# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyLightningUtilities(PythonPackage):
    """Common Python utilities and GitHub Actions in Lightning Ecosystem"""

    homepage = "https://github.com/Lightning-AI/utilities"
    pypi = "lightning-utilities/lightning-utilities-0.4.1.tar.gz"

    maintainers("adamjstewart")

    license("Apache-2.0")

    version(
        "0.8.0",
        sha256="22aa107b51c8f50ccef54d08885eb370903eb04148cddb2891b9c65c59de2a6e",
        url="https://pypi.org/packages/5d/ec/a20c5d5f26894913da028110310ba55ee254e1b7ff0ff78441e4eeb7291f/lightning_utilities-0.8.0-py3-none-any.whl",
    )
    version(
        "0.6.0.post0",
        sha256="81edf3ce5ebd43389238afc1bca96ea0c6dcd3b4b442f8365c719dd3a82009dc",
        url="https://pypi.org/packages/52/9c/104b3c799cde4b23d2754409ba7c1f856f1406d74657287f53f6409f8231/lightning_utilities-0.6.0.post0-py3-none-any.whl",
    )
    version(
        "0.5.0",
        sha256="db1fa4300ce76b171d8cd4e78ffad3b6bc82f3fbe8ca5aa35da269fbda65bea3",
        url="https://pypi.org/packages/f2/37/0c1e403717ad981f1ae407771a4e6f6be4407ed4f532b5c41703d5a33104/lightning_utilities-0.5.0-py3-none-any.whl",
    )
    version(
        "0.4.2",
        sha256="397fd573b406408e9d3d376b2b728dba44b0517dd487401a3117f96e434d0afc",
        url="https://pypi.org/packages/a0/66/14312d4b9318d9500146528d4ac4f313b19d94d90615e5599cce089967e2/lightning_utilities-0.4.2-py3-none-any.whl",
    )
    version(
        "0.4.1",
        sha256="880bbdff34ff7d3ca042b7d6ff0cc4bda1f9079a648752db654beefb6e754b03",
        url="https://pypi.org/packages/7e/ea/40e64439ad0869663c106de30cd4656254ad046a5871f1d45be326f5ed90/lightning_utilities-0.4.1-py3-none-any.whl",
    )
    version(
        "0.4.0",
        sha256="36d257f9eb9e1cb2669a43ca200d1dd4a0b4840768b38d9f69a892ff004cb412",
        url="https://pypi.org/packages/67/17/bed12398a0417be28970bb3f8252a36ae0b2bc0d580b0dcddf6ad5d89a62/lightning_utilities-0.4.0-py3-none-any.whl",
    )
    version(
        "0.3.0",
        sha256="1ae9bdd8f1be3c81b1ac4820f6eeddcbafcc2505c57a5940054466f4763bc22d",
        url="https://pypi.org/packages/8f/fc/1f4ff2bcba4e6162276cabe831a431ef14681a7158e693a5cf828dd6fa1b/lightning_utilities-0.3.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:", when="@0.2:0.10")
        depends_on("py-fire", when="@0.2:0.3")
        depends_on("py-importlib-metadata@4:", when="@0.4.1: ^python@:3.7")
        depends_on("py-packaging@17.1:", when="@0.6.0.post:")
        depends_on("py-packaging@20:", when="@0.5:0.6.0.0")
        depends_on("py-typing-extensions", when="@0.5:")

    # setup.py

    # requirements/base.txt

    # Historical dependencies

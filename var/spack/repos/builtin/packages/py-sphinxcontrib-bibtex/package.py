# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySphinxcontribBibtex(PythonPackage):
    """A Sphinx extension for BibTeX style citations."""

    pypi = "sphinxcontrib-bibtex/sphinxcontrib-bibtex-0.3.5.tar.gz"

    version(
        "2.5.0",
        sha256="748f726eaca6efff7731012103417ef130ecdcc09501b4d0c54283bf5f059f76",
        url="https://pypi.org/packages/b2/17/3be04de2ed752996654895558db01a30d64759b2c7120e7692402b8d4e19/sphinxcontrib_bibtex-2.5.0-py3-none-any.whl",
    )
    version(
        "2.4.2",
        sha256="608512afde6b732148cdc9123550bd560bf48e071d1fb7bb1bab4f4437ff04f4",
        url="https://pypi.org/packages/44/cc/9b30e4b255da07ee8434eb13b02199f2b53003fa1b45b2a2bfbd5a179e4f/sphinxcontrib_bibtex-2.4.2-py3-none-any.whl",
    )
    version(
        "2.2.1",
        sha256="38e8e9e1d450b50f33b2e42855da66e7c71e7ea533ca2a381b6d8d6314975a36",
        url="https://pypi.org/packages/93/07/fcfae00f1325491fce51c6358a6913a3c48b7095670a9aa747666dca8bfa/sphinxcontrib_bibtex-2.2.1-py3-none-any.whl",
    )
    version(
        "2.2.0",
        sha256="f35c1a75826c1b0dd1c680bb144c774630dcf5f78f1501a8c68cdfa8381a4e87",
        url="https://pypi.org/packages/af/26/d4cc2f5bc2d551fb0e63b1de14677a7986bae6a70f37e154379cb0916da7/sphinxcontrib_bibtex-2.2.0-py3-none-any.whl",
    )
    version(
        "2.1.4",
        sha256="f8a0625e1367b8fba243af48990b9a487b12388a470a4fd91daf3e06720aa287",
        url="https://pypi.org/packages/0e/13/24b1d6481e94143b5900c82ccac6de398d9f40ad0b42b5afc56ee3527eba/sphinxcontrib_bibtex-2.1.4-py3-none-any.whl",
    )
    version(
        "2.0.0",
        sha256="2e1d36fc2a0820dff342c21c44125a142ca1835a54a3b4a92bf09aeabbd7eb5f",
        url="https://pypi.org/packages/b7/f1/96b86e5f27d13c3f558bc2f2f82787d296ba414673eb6c9cdc7297410d83/sphinxcontrib_bibtex-2.0.0-py3-none-any.whl",
    )
    version(
        "1.0.0",
        sha256="bebc2cba91e838f808c49dbf5735812525a11221a9b134fa4cc366990f85c864",
        url="https://pypi.org/packages/60/de/831ec5de791ba30b842a26e27c479ed34259fb1823aa681d8028c551f4d0/sphinxcontrib_bibtex-1.0.0-py3-none-any.whl",
    )
    version(
        "0.3.5",
        sha256="16cc1ee34224e57c58fdf26d2afbf57c982855bf0e5bcb4b37b235bee3989bda",
        url="https://pypi.org/packages/fd/82/2b49e44eff94db4ed6ae9b7729c47705b17dc05ec47339430dcadbd5df4b/sphinxcontrib_bibtex-0.3.5-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-dataclasses", when="@2.2: ^python@:3.6")
        depends_on("py-docutils@0.8:", when="@2.1:2.5")
        depends_on("py-importlib-metadata@3.6:", when="@2.5: ^python@:3.9")
        depends_on("py-oset@0.1.3:", when="@0.4:2.0")
        depends_on("py-pybtex@0.24:", when="@2.4.2:")
        depends_on("py-pybtex@0.20:", when="@0.4:2.4.1")
        depends_on("py-pybtex-docutils@1:", when="@2.2:")
        depends_on("py-pybtex-docutils@0.2.2:", when="@2:2.1")
        depends_on("py-pybtex-docutils@0.2:", when="@0.4:1")
        depends_on("py-sphinx@2.1:", when="@2.1.3:2.5")
        depends_on("py-sphinx@2.0.0:", when="@1:2.1.2")

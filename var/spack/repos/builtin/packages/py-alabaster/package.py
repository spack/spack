# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAlabaster(PythonPackage):
    """Alabaster is a visually (c)lean, responsive, configurable theme
    for the Sphinx documentation system."""

    homepage = "https://alabaster.readthedocs.io/"
    pypi = "alabaster/alabaster-0.7.10.tar.gz"
    git = "https://github.com/sphinx-doc/alabaster.git"

    version(
        "0.7.13",
        sha256="1ee19aca801bbabb5ba3f5f258e4422dfa86f82f3e9cefb0859b283cdd7f62a3",
        url="https://pypi.org/packages/64/88/c7083fc61120ab661c5d0b82cb77079fc1429d3f913a456c1c82cf4658f7/alabaster-0.7.13-py3-none-any.whl",
    )
    version(
        "0.7.12",
        sha256="446438bdcca0e05bd45ea2de1668c1d9b032e1a9154c2c259092d77031ddd359",
        url="https://pypi.org/packages/10/ad/00b090d23a222943eb0eda509720a404f531a439e803f6538f35136cae9e/alabaster-0.7.12-py2.py3-none-any.whl",
    )
    version(
        "0.7.10",
        sha256="2eef172f44e8d301d25aff8068fddd65f767a3f04b5f15b0f4922f113aa1c732",
        url="https://pypi.org/packages/2e/c3/9b7dcd8548cf2c00531763ba154e524af575e8f36701bacfe5bcadc67440/alabaster-0.7.10-py2.py3-none-any.whl",
    )
    version(
        "0.7.9",
        sha256="d3e64a74919373d6d4d1d36bd717206584cb64cbb0532dfce3bc2081cba6817b",
        url="https://pypi.org/packages/5d/da/2e59e6b040f1062843eb9e874f504bc6779053b77da5d1ed7f1b46618e13/alabaster-0.7.9-py2.py3-none-any.whl",
    )

# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPy4j(PythonPackage):
    """Enables Python programs to dynamically access arbitrary Java
    objects."""

    homepage = "https://www.py4j.org/"
    pypi = "py4j/py4j-0.10.4.zip"

    license("BSD-3-Clause")

    version(
        "0.10.9.5",
        sha256="52d171a6a2b031d8a5d1de6efe451cf4f5baff1a2819aabc3741c8406539ba04",
        url="https://pypi.org/packages/86/ec/60880978512d5569ca4bf32b3b4d7776a528ecf4bca4523936c98c92a3c8/py4j-0.10.9.5-py2.py3-none-any.whl",
    )
    version(
        "0.10.9.3",
        sha256="04f5b06917c0c8a81ab34121dda09a2ba1f74e96d59203c821d5cb7d28c35363",
        url="https://pypi.org/packages/5e/e6/68db58a1d94d41ae042400f7965ed6a2c30e4108f77b54672d6451f86ebd/py4j-0.10.9.3-py2.py3-none-any.whl",
    )
    version(
        "0.10.9",
        sha256="859ba728a7bb43e9c2bf058832759fb97a598bb28cc12f34f5fc4abdec08ede6",
        url="https://pypi.org/packages/9e/b6/6a4fb90cd235dc8e265a6a2067f2a2c99f0d91787f06aca4bcf7c23f3f80/py4j-0.10.9-py2.py3-none-any.whl",
    )
    version(
        "0.10.7",
        sha256="a950fe7de1bfd247a0a4dddb9118f332d22a89e01e0699135ea8038c15ee1293",
        url="https://pypi.org/packages/e3/53/c737818eb9a7dc32a7cd4f1396e787bd94200c3997c72c1dbe028587bd76/py4j-0.10.7-py2.py3-none-any.whl",
    )
    version(
        "0.10.6",
        sha256="3ede9c975803a3f1df6c4850349c0179f17c2380e2917b8a574f7f37e8c43f4b",
        url="https://pypi.org/packages/4a/08/162710786239aa72bd72bb46c64f2b02f54250412ba928cb373b30699139/py4j-0.10.6-py2.py3-none-any.whl",
    )
    version(
        "0.10.4",
        sha256="784d57e3e68bf45b6b40b7f7df52109e3f6ee37b553c58574901526b1153400e",
        url="https://pypi.org/packages/93/a7/0e1719e8ad34d194aae72dc07a37e65fd3895db7c797a67a828333cd6067/py4j-0.10.4-py2.py3-none-any.whl",
    )
    version(
        "0.10.3",
        sha256="348e7bd7047c659bea7cff57350f0f00cd1deeea5369e9e8ddb038ea57915823",
        url="https://pypi.org/packages/3b/21/5f7907f6a678a3527b363de3f16482206fe06aa23c68a54c089faef2d04c/py4j-0.10.3-py2.py3-none-any.whl",
    )

# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyHatchling(PythonPackage):
    """Modern, extensible Python build backend."""

    homepage = "https://hatch.pypa.io/latest/"
    pypi = "hatchling/hatchling-1.4.1.tar.gz"
    git = "https://github.com/pypa/hatch"

    license("MIT", checked_by="tgamblin")

    version(
        "1.21.0",
        sha256="b33ef0ecdee6dbfd28c21ca30df459ba1d566050d033f8b5a1d0e26e5606d26b",
        url="https://pypi.org/packages/04/35/aa8738d6674aba09d3f0c77a1c40aee1dbf10e1b26d03cbd987aa6642e86/hatchling-1.21.0-py3-none-any.whl",
    )
    version(
        "1.18.0",
        sha256="b66dc254931ec42aa68b5febd1d342c58142cc5267b7ff3b12ba3fa5b4900c93",
        url="https://pypi.org/packages/76/56/8ccca673e2c896931722f876bf040c0b6a7d8c1a128be60516a8a55bb27a/hatchling-1.18.0-py3-none-any.whl",
    )
    version(
        "1.17.0",
        sha256="2d022a72a027de26e783b3a597bd046a6ead8edd435ea29ee87a20d60bfea1fe",
        url="https://pypi.org/packages/30/28/58bc90ec306e18881c3cb75084a6a203ad974829c1b5ac81dda4e58cf2a8/hatchling-1.17.0-py3-none-any.whl",
    )
    version(
        "1.14.0",
        sha256="545163d58ab1f908dd1bb1092432738848329d5eaadedb4b38b6bc1f37d9b4ea",
        url="https://pypi.org/packages/d0/a2/58a005a7fe8d0c23bc8905ad9f17e4921f5378e18d34f9279b5345987543/hatchling-1.14.0-py3-none-any.whl",
    )
    version(
        "1.13.0",
        sha256="357d5a5abac0d28e24fa87534efc63f5ba3f9b3306675678049ca4ba9f2a6674",
        url="https://pypi.org/packages/2a/8a/a2d2b9f93d382ad3d805847f74b33ed38da2eaac2bcf82686c55d3450f80/hatchling-1.13.0-py3-none-any.whl",
    )
    version(
        "1.10.0",
        sha256="fb28c3106247022da0e794899502e3164d4a3ccf8f55b1826ff72ee1af087046",
        url="https://pypi.org/packages/26/d3/fca2fb066cd41967b6f0041bc57c34d02aeef43f23590875618635afbc0c/hatchling-1.10.0-py3-none-any.whl",
    )
    version(
        "1.8.1",
        sha256="09171ed1404e636ef572b370d34c5cb36a8029825c0a7859ac93989080ba2630",
        url="https://pypi.org/packages/19/93/bd81c789331a317351b2887a508843804de1414d9455a37bce78f6722c25/hatchling-1.8.1-py3-none-any.whl",
    )
    version(
        "1.4.1",
        sha256="c26200c9ec13f58ffb48bfb067ffd6bb90ba4d9c24f1d7e932ef58aa9621477d",
        url="https://pypi.org/packages/5e/fc/8265418d0605309e7458a1dd63c7071920763a40578be50a0aa9800d7b28/hatchling-1.4.1-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.8:", when="@1.18:")
        depends_on("python@3.7:", when="@1:1.17")
        depends_on("py-editables@0.3:", when="@:1.21")
        depends_on("py-importlib-metadata", when="@:1.17 ^python@:3.7")
        depends_on("py-packaging@21.3:")
        depends_on("py-pathspec@0.10.1:", when="@1.9:")
        depends_on("py-pathspec@0.9:", when="@:1.8")
        depends_on("py-pluggy@1:1.0.0.0,1.1:")
        depends_on("py-tomli@1.2.2:", when="^python@:3.10")
        depends_on("py-trove-classifiers", when="@1.14:")

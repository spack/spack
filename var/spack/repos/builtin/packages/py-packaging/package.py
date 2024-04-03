# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPackaging(PythonPackage):
    """Core utilities for Python packages."""

    homepage = "https://github.com/pypa/packaging"
    pypi = "packaging/packaging-19.2.tar.gz"

    license("BSD-2-Clause")

    version(
        "23.1",
        sha256="994793af429502c4ea2ebf6bf664629d07c1a9fe974af92966e4b8d2df7edc61",
        url="https://pypi.org/packages/ab/c3/57f0601a2d4fe15de7a553c00adbc901425661bf048f2a22dfc500caf121/packaging-23.1-py3-none-any.whl",
    )
    version(
        "23.0",
        sha256="714ac14496c3e68c99c29b00845f7a2b85f3bb6f1078fd9f72fd20f0570002b2",
        url="https://pypi.org/packages/ed/35/a31aed2993e398f6b09a790a181a7927eb14610ee8bbf02dc14d31677f1c/packaging-23.0-py3-none-any.whl",
    )
    version(
        "21.3",
        sha256="ef103e05f519cdc783ae24ea4e2e0f508a9c99b2d4969652eed6a2e1ea5bd522",
        url="https://pypi.org/packages/05/8e/8de486cbd03baba4deef4142bd643a3e7bbe954a784dc1bb17142572d127/packaging-21.3-py3-none-any.whl",
    )
    version(
        "21.0",
        sha256="c86254f9220d55e31cc94d69bade760f0847da8000def4dfe1c6b872fd14ff14",
        url="https://pypi.org/packages/3c/77/e2362b676dc5008d81be423070dd9577fa03be5da2ba1105811900fda546/packaging-21.0-py3-none-any.whl",
    )
    version(
        "20.9",
        sha256="67714da7f7bc052e064859c05c595155bd1ee9f69f76557e21f051443c20947a",
        url="https://pypi.org/packages/3e/89/7ea760b4daa42653ece2380531c90f64788d979110a2ab51049d92f408af/packaging-20.9-py2.py3-none-any.whl",
    )
    version(
        "19.2",
        sha256="d9551545c6d761f3def1677baf08ab2a3ca17c56879e70fecba2fc4dde4ed108",
        url="https://pypi.org/packages/cf/94/9672c2d4b126e74c4496c6b3c58a8b51d6419267be9e70660ba23374c875/packaging-19.2-py2.py3-none-any.whl",
    )
    version(
        "19.1",
        sha256="a7ac867b97fdc07ee80a8058fe4435ccd274ecc3b0ed61d852d7d53055528cf9",
        url="https://pypi.org/packages/ec/22/630ac83e8f8a9566c4f88038447ed9e16e6f10582767a01f31c769d9a71e/packaging-19.1-py2.py3-none-any.whl",
    )
    version(
        "19.0",
        sha256="9e1cbf8c12b1f1ce0bb5344b8d7ecf66a6f8a6e91bcb0c84593ed6d3ab5c4ab3",
        url="https://pypi.org/packages/91/32/58bc30e646e55eab8b21abf89e353f59c0cc02c417e42929f4a9546e1b1d/packaging-19.0-py2.py3-none-any.whl",
    )
    version(
        "17.1",
        sha256="e9215d2d2535d3ae866c3d6efc77d5b24a0192cce0ff20e42896cc0664f889c0",
        url="https://pypi.org/packages/ad/c2/b500ea05d5f9f361a562f089fc91f77ed3b4783e13a08a3daf82069b1224/packaging-17.1-py2.py3-none-any.whl",
    )
    version(
        "16.8",
        sha256="99276dc6e3a7851f32027a68f1095cd3f77c148091b092ea867a351811cfe388",
        url="https://pypi.org/packages/87/1b/c39b7c65b5612812b83d6cab7ef2885eac9f6beb0b7b8a7071a186aea3b1/packaging-16.8-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:", when="@22:")
        depends_on("py-attrs", when="@19.1")
        depends_on("py-pyparsing@2.0.2:3.0.4,3.0.6:", when="@21.3:21")
        depends_on("py-pyparsing@2.0.2:", when="@17:21.0")
        depends_on("py-pyparsing", when="@16")
        depends_on("py-six", when="@16.1:20.4")

    # Needed to bootstrap Spack correctly on Python 3.6 (rhel8 platform-python)

    # Historical dependencies

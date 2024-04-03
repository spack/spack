# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyApispec(PythonPackage):
    """A pluggable API specification generator."""

    homepage = "https://github.com/marshmallow-code/apispec"
    pypi = "apispec/apispec-6.0.2.tar.gz"

    license("MIT")

    version(
        "6.0.2",
        sha256="d97f0ae9c65133185b9ed9c5be1a434eb85627dfa33c4c53cabda122256c1b67",
        url="https://pypi.org/packages/06/05/397d3da7d64c095d38d75b95aacd76d22f7491184f7e2910e8ce79f068f8/apispec-6.0.2-py3-none-any.whl",
    )
    version(
        "4.7.1",
        sha256="6613dbc39f41cd58942a697f11c8762ba18422bd173fe0bdfc1535b83d3f84f0",
        url="https://pypi.org/packages/3f/5b/312dd28e8e0b94dfe3c41db5a5c83a944c938a2108d631613fa0bbe3c8f7/apispec-4.7.1-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:", when="@5.2:6.3")
        depends_on("py-packaging@21.3:", when="@6:")

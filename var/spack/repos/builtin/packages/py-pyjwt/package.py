# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyjwt(PythonPackage):
    """JSON Web Token implementation in Python"""

    homepage = "https://github.com/jpadilla/pyjwt"
    pypi = "PyJWT/PyJWT-1.7.1.tar.gz"

    license("MIT")

    version(
        "2.4.0",
        sha256="72d1d253f32dbd4f5c88eaf1fdc62f3a19f676ccbadb9dbc5d07e951b2b26daf",
        url="https://pypi.org/packages/1c/fb/b82e9601b00d88cf8bbee1f39b855ae773f9d5bcbcedb3801b2f72460696/PyJWT-2.4.0-py3-none-any.whl",
    )
    version(
        "2.1.0",
        sha256="934d73fbba91b0483d3857d1aff50e96b2a892384ee2c17417ed3203f173fca1",
        url="https://pypi.org/packages/3f/32/d5d3cab27fee7f6b22d7cd7507547ae45d52e26030fa77d1f83d0526c6e5/PyJWT-2.1.0-py3-none-any.whl",
    )
    version(
        "1.7.1",
        sha256="5c6eca3c2940464d106b99ba83b00c6add741c9becaec087fb7ccdefea71350e",
        url="https://pypi.org/packages/87/8b/6a9f14b5f781697e51259d81657e6048fd31a113229cf346880bb7545565/PyJWT-1.7.1-py2.py3-none-any.whl",
    )

    variant("crypto", default=False, description="Build with cryptography support")

    with default_args(type="run"):
        depends_on("py-cryptography@3.3.1:", when="@2.2:2.5+crypto")
        depends_on("py-cryptography@3.3.1:3", when="@2.0.0:2.1+crypto")
        depends_on("py-cryptography@1.4:", when="@1.5.3:1+crypto")

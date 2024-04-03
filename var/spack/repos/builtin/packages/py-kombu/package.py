# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyKombu(PythonPackage):
    """Messaging library for Python."""

    pypi = "kombu/kombu-4.3.0.tar.gz"

    license("BSD-3-Clause")

    version(
        "5.2.3",
        sha256="eeaeb8024f3a5cfc71c9250e45cddb8493f269d74ada2f74909a93c59c4b4179",
        url="https://pypi.org/packages/6b/e6/79f5fc77b8f54de7e3d8bdf382b2ca23e85ed35095801851003e70028f2f/kombu-5.2.3-py3-none-any.whl",
    )
    version(
        "5.0.2",
        sha256="6dc509178ac4269b0e66ab4881f70a2035c33d3a622e20585f965986a5182006",
        url="https://pypi.org/packages/22/6e/69bc1061633a88aa47beaa8bbecff1c3c555a005603cfbebcec4aa37f183/kombu-5.0.2-py2.py3-none-any.whl",
    )
    version(
        "4.6.11",
        sha256="be48cdffb54a2194d93ad6533d73f69408486483d189fe9f5990ee24255b0e0a",
        url="https://pypi.org/packages/9e/34/3eea6a3a9ff81b0c7ddbdceb22a1ffc1b5907d863f27ca19a68777d2211d/kombu-4.6.11-py2.py3-none-any.whl",
    )
    version(
        "4.6.6",
        sha256="e7465aa85a1db889116819f08c5de29520d2fa103324dcdca5e90af345f01771",
        url="https://pypi.org/packages/f7/86/496db94e44c6d0a16a52a1b539b5315d98e8aa59d14a8d4f1009d4eab6c2/kombu-4.6.6-py2.py3-none-any.whl",
    )
    version(
        "4.5.0",
        sha256="7b92303af381ef02fad6899fd5f5a9a96031d781356cd8e505fa54ae5ddee181",
        url="https://pypi.org/packages/b7/af/1914e93314f1b98756d5c5e366193124a0ffaab0e6d0e51e0f6f65fa851d/kombu-4.5.0-py2.py3-none-any.whl",
    )
    version(
        "4.3.0",
        sha256="7a2cbed551103db9a4e2efafe9b63222e012a61a18a881160ad797b9d4e1d0a1",
        url="https://pypi.org/packages/29/48/c709a54c8533ed46fd868e593782c6743da33614f8134b82bc0955455031/kombu-4.3.0-py2.py3-none-any.whl",
    )

    variant("redis", default=False, description="Use redis transport")

    with default_args(type="run"):
        depends_on("python@3.7:", when="@5.2.0:5.3.0-beta3")
        depends_on("py-amqp@5.0.9:", when="@5.2.3:5.2")
        depends_on("py-amqp@5.0.0:", when="@5.0.2:5.0")
        depends_on("py-amqp@2.6:2", when="@4.6.9:5.0.1")
        depends_on("py-amqp@2.5.2:2.5", when="@4.6.6:4.6.8")
        depends_on("py-amqp@2.4:2", when="@4.3:4.5")
        depends_on("py-cached-property", when="@5.1:5.3.0-beta3 ^python@:3.7")
        depends_on("py-importlib-metadata@0.18:", when="@4.6.7:5.3.0-beta1 ^python@:3.7")
        depends_on("py-importlib-metadata@0.18:", when="@4.6.4:4.6.6")
        depends_on("py-redis@3.4.1:4.0.0-rc2,4.0.2:", when="@5.2.3:5.2+redis")
        depends_on("py-redis@3.3.11:", when="@4.6.6:5.2.0+redis")
        depends_on("py-redis@3.2:", when="@4.4:4.6.5+redis")
        depends_on("py-redis@2.10.5:", when="@4.2:4.3+redis")
        depends_on("py-vine", when="@5.1:")

    # "pytz>dev" in tests_require: setuptools parser changed in v60 and errors.

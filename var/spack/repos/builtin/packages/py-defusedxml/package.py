# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDefusedxml(PythonPackage):
    """defusing XML bombs and other exploits"""

    homepage = "https://github.com/tiran/defusedxml"
    pypi = "defusedxml/defusedxml-0.5.0.tar.gz"

    license("PSF-2.0")

    version(
        "0.7.1",
        sha256="a352e7e428770286cc899e2542b6cdaedb2b4953ff269a210103ec58f6198a61",
        url="https://pypi.org/packages/07/6c/aa3f2f849e01cb6a001cd8554a88d4c77c5c1a31c95bdf1cf9301e6d9ef4/defusedxml-0.7.1-py2.py3-none-any.whl",
    )
    version(
        "0.6.0",
        sha256="6687150770438374ab581bb7a1b327a847dd9c5749e396102de3fad4e8a3ef93",
        url="https://pypi.org/packages/06/74/9b387472866358ebc08732de3da6dc48e44b0aacd2ddaa5cb85ab7e986a2/defusedxml-0.6.0-py2.py3-none-any.whl",
    )
    version(
        "0.5.0",
        sha256="702a91ade2968a82beb0db1e0766a6a273f33d4616a6ce8cde475d8e09853b20",
        url="https://pypi.org/packages/87/1c/17f3e3935a913dfe2a5ca85fa5ccbef366bfd82eb318b1f75dadbf0affca/defusedxml-0.5.0-py2.py3-none-any.whl",
    )

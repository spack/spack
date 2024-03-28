# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyasn1(PythonPackage):
    """Pure-Python implementation of ASN.1 types and DER/BER/CER codecs
    (X.208)."""

    homepage = "https://github.com/etingof/pyasn1"
    pypi = "pyasn1/pyasn1-0.4.6.tar.gz"

    license("BSD-2-Clause")

    version(
        "0.4.8",
        sha256="39c7e2ec30515947ff4e87fb6f456dfc6e84857d34be479c9d4a4ba4bf46aa5d",
        url="https://pypi.org/packages/62/1e/a94a8d635fa3ce4cfc7f506003548d0a2447ae76fd5ca53932970fe3053f/pyasn1-0.4.8-py2.py3-none-any.whl",
    )
    version(
        "0.4.6",
        sha256="3bb81821d47b17146049e7574ab4bf1e315eb7aead30efe5d6a9ca422c9710be",
        url="https://pypi.org/packages/6a/6e/209351ec34b7d7807342e2bb6ff8a96eef1fd5dcac13bdbadf065c2bb55c/pyasn1-0.4.6-py2.py3-none-any.whl",
    )
    version(
        "0.4.5",
        sha256="da6b43a8c9ae93bc80e2739efb38cc776ba74a886e3e9318d65fe81a8b8a2c6e",
        url="https://pypi.org/packages/7b/7c/c9386b82a25115cccf1903441bba3cbadcfae7b678a20167347fa8ded34c/pyasn1-0.4.5-py2.py3-none-any.whl",
    )
    version(
        "0.4.3",
        sha256="a66dcda18dbf6e4663bde70eb30af3fc4fe1acb2d14c4867a861681887a5f9a2",
        url="https://pypi.org/packages/a0/70/2c27740f08e477499ce19eefe05dbcae6f19fdc49e9e82ce4768be0643b9/pyasn1-0.4.3-py2.py3-none-any.whl",
    )
    version(
        "0.2.3",
        sha256="0439b9bd518418260c2641a571f0e07fce4370cab13b68f19b5e023306c03cad",
        url="https://pypi.org/packages/a5/ae/6b4c4cb9420edddd7401782f55504130d1269f2e5ae3ba3c986da167dd6c/pyasn1-0.2.3-py2.py3-none-any.whl",
    )

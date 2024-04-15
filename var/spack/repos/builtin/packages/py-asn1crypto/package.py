# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAsn1crypto(PythonPackage):
    """Python ASN.1 library with a focus on performance and a pythonic API"""

    homepage = "https://github.com/wbond/asn1crypto"
    pypi = "asn1crypto/asn1crypto-0.22.0.tar.gz"

    license("MIT")

    version(
        "1.5.1",
        sha256="db4e40728b728508912cbb3d44f19ce188f218e9eba635821bb4b68564f8fd67",
        url="https://pypi.org/packages/c9/7f/09065fd9e27da0eda08b4d6897f1c13535066174cc023af248fc2a8d5e5a/asn1crypto-1.5.1-py2.py3-none-any.whl",
    )
    version(
        "1.4.0",
        sha256="4bcdf33c861c7d40bdcd74d8e4dd7661aac320fcdf40b9a3f95b4ee12fde2fa8",
        url="https://pypi.org/packages/b5/a8/56be92dcd4a5bf1998705a9b4028249fe7c9a035b955fe93b6a3e5b829f8/asn1crypto-1.4.0-py2.py3-none-any.whl",
    )
    version(
        "0.24.0",
        sha256="2f1adbb7546ed199e3c90ef23ec95c5cf3585bac7d11fb7eb562a3fe89c64e87",
        url="https://pypi.org/packages/ea/cd/35485615f45f30a510576f1a56d1e0a7ad7bd8ab5ed7cdc600ef7cd06222/asn1crypto-0.24.0-py2.py3-none-any.whl",
    )
    version(
        "0.22.0",
        sha256="d232509fefcfcdb9a331f37e9c9dc20441019ad927c7d2176cf18ed5da0ba097",
        url="https://pypi.org/packages/97/ba/7e8117d8efcee589f4d96dd2b2eb1d997f96d27d214cf2b7134ad8acf6ab/asn1crypto-0.22.0-py2.py3-none-any.whl",
    )

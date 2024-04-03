# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyParso(PythonPackage):
    """Parso is a Python parser that supports error recovery and round-trip parsing
    for different Python versions (in multiple Python versions).
    Parso is also able to list multiple syntax errors
    in your python file."""

    pypi = "parso/parso-0.6.1.tar.gz"

    license("MIT")

    version(
        "0.8.3",
        sha256="c001d4636cd3aecdaf33cbb40aebb59b094be2a74c556778ef5576c175e19e75",
        url="https://pypi.org/packages/05/63/8011bd08a4111858f79d2b09aad86638490d62fbf881c44e434a6dfca87b/parso-0.8.3-py2.py3-none-any.whl",
    )
    version(
        "0.8.2",
        sha256="a8c4922db71e4fdb90e0d0bc6e50f9b273d3397925e5e60a717e719201778d22",
        url="https://pypi.org/packages/a9/c4/d5476373088c120ffed82f34c74b266ccae31a68d665b837354d4d8dc8be/parso-0.8.2-py2.py3-none-any.whl",
    )
    version(
        "0.8.1",
        sha256="15b00182f472319383252c18d5913b69269590616c947747bc50bf4ac768f410",
        url="https://pypi.org/packages/ad/f0/ef6bdb1eba2dbfda60c985cd8d7b47b6ed8c6a1f5d212f39ff50b64f172c/parso-0.8.1-py2.py3-none-any.whl",
    )
    version(
        "0.7.1",
        sha256="97218d9159b2520ff45eb78028ba8b50d2bc61dcc062a9682666f2dc4bd331ea",
        url="https://pypi.org/packages/93/d1/e635bdde32890db5aeb2ffbde17e74f68986305a4466b0aa373b861e3f00/parso-0.7.1-py2.py3-none-any.whl",
    )
    version(
        "0.6.1",
        sha256="951af01f61e6dccd04159042a0706a31ad437864ec6e25d0d7a96a9fbb9b0095",
        url="https://pypi.org/packages/ec/bb/3b6c9f604ac40e2a7833bc767bd084035f12febcbd2b62204c5bc30edf97/parso-0.6.1-py2.py3-none-any.whl",
    )
    version(
        "0.4.0",
        sha256="17cc2d7a945eb42c3569d4564cdf49bde221bc2b552af3eca9c1aad517dcdd33",
        url="https://pypi.org/packages/a7/bd/e2f4753c5fa93932899243b4299011a757ac212e9bc8ddf062f38df4e78b/parso-0.4.0-py2.py3-none-any.whl",
    )

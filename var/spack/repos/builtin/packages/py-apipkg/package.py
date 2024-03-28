# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyApipkg(PythonPackage):
    """apipkg: namespace control and lazy-import mechanism"""

    pypi = "apipkg/apipkg-1.4.tar.gz"

    license("MIT")

    version(
        "1.5",
        sha256="58587dd4dc3daefad0487f6d9ae32b4542b185e1c36db6993290e7c41ca2b47c",
        url="https://pypi.org/packages/67/08/4815a09603fc800209431bec5b8bd2acf2f95abdfb558a44a42507fb94da/apipkg-1.5-py2.py3-none-any.whl",
    )
    version(
        "1.4",
        sha256="65d2aa68b28e7d31233bb2ba8eb31cda40e4671f8ac2d6b241e358c9652a74b9",
        url="https://pypi.org/packages/94/72/fd4f2e46ce7b0d388191c819ef691c8195fab09602bbf1a2f92aa5351444/apipkg-1.4-py2.py3-none-any.whl",
    )

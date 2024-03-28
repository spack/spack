# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySniffio(PythonPackage):
    """This is a tiny package whose only purpose is to let you detect which
    async library your code is running under."""

    homepage = "https://github.com/python-trio/sniffio"
    pypi = "sniffio/sniffio-1.1.0.tar.gz"

    license("Apache-2.0")

    version(
        "1.3.0",
        sha256="eecefdce1e5bbfb7ad2eeaabf7c1eeb404d7757c379bd1f7e5cce9d8bf425384",
        url="https://pypi.org/packages/c3/a0/5dba8ed157b0136607c7f2151db695885606968d1fae123dc3391e0cfdbf/sniffio-1.3.0-py3-none-any.whl",
    )
    version(
        "1.2.0",
        sha256="471b71698eac1c2112a40ce2752bb2f4a4814c22a54a3eed3676bc0f5ca9f663",
        url="https://pypi.org/packages/52/b0/7b2e028b63d092804b6794595871f936aafa5e9322dcaaad50ebf67445b3/sniffio-1.2.0-py3-none-any.whl",
    )
    version(
        "1.1.0",
        sha256="20ed6d5b46f8ae136d00b9dcb807615d83ed82ceea6b2058cecb696765246da5",
        url="https://pypi.org/packages/b3/82/4bd4b7d9c0d1dc0fbfbc2a1e00138e7f3ab85bc239358fe9b78aa2ab586d/sniffio-1.1.0-py3-none-any.whl",
    )

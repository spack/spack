# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPy4j(PythonPackage):
    """Enables Python programs to dynamically access arbitrary Java
    objects."""

    homepage = "https://www.py4j.org/"
    pypi = "py4j/py4j-0.10.4.zip"

    version(
        "0.10.9.5",
        url="https://files.pythonhosted.org/packages/ce/1f/b00295b6da3bd2f050912b9f71fdb436ae8f1601cf161365937d8553e24b/py4j-0.10.9.5.tar.gz",
        sha256="276a4a3c5a2154df1860ef3303a927460e02e97b047dc0a47c1c3fb8cce34db6",
    )
    version(
        "0.10.9.3",
        url="https://files.pythonhosted.org/packages/d1/c4/9674152db7bb6dd67e5c93eeb48b727a840551932c88a44e20143cb661c1/py4j-0.10.9.3.tar.gz",
        sha256="0d92844da4cb747155b9563c44fc322c9a1562b3ef0979ae692dbde732d784dd",
    )

    version(
        "0.10.9",
        url="https://files.pythonhosted.org/packages/10/ed/9dad8808c34bc5b0b1a44b13c0bddeea0c8df59956eb20ac2fecc373f322/py4j-0.10.9.tar.gz",
        sha256="36ec57f43ff8ced260a18aa9a4e46c3500a730cac8860e259cbaa546c2b9db2f",
    )
    version("0.10.7", sha256="721189616b3a7d28212dfb2e7c6a1dd5147b03105f1fc37ff2432acd0e863fa5")
    version("0.10.6", sha256="d3e7ac7c2171c290eba87e70aa5095b7eb6d6ad34789c007c88d550d9f575083")
    version("0.10.4", sha256="406fbfdbcbbb398739f61fafd25724670a405a668eb08c1721d832eadce06aae")
    version("0.10.3", sha256="f4570108ad014dd52a65c2288418e31cb8227b5ecc39ad7fc7fe98314f7a26f2")

    depends_on("py-setuptools", type="build")

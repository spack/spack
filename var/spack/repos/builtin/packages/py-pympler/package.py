# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPympler(PythonPackage):
    """Development tool to measure, monitor and analyze the memory behavior
    of Python objects in a running Python application.
    """

    homepage = "https://github.com/pympler/pympler"
    pypi = "Pympler/Pympler-0.4.3.tar.gz"

    license("Apache-2.0")

    version(
        "1.0.1",
        sha256="d260dda9ae781e1eab6ea15bacb84015849833ba5555f141d2d9b7b7473b307d",
        url="https://pypi.org/packages/2c/42/41e1469ed0b37b9c8532cb8074bea179f7d85ee7e82a59b5b6c289ed6045/Pympler-1.0.1-py3-none-any.whl",
    )

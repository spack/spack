# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPgzip(PythonPackage):
    """A multi-threading implementation of Python gzip module"""

    homepage = "https://github.com/pgzip/pgzip"
    pypi = "pgzip/pgzip-0.3.4.tar.gz"

    license("MIT")

    version(
        "0.3.4",
        sha256="cf3e5963262fd2c7ba16a5a60120ae13469c7e207e7739e968482d5ae444d435",
        url="https://pypi.org/packages/82/27/dc9d8a67be31c71b46e9b7df75e000806ca9aa94929d42976fd5b82d7a9d/pgzip-0.3.4-py3-none-any.whl",
    )
    version(
        "0.3.1",
        sha256="eb1430014e58f69b60f93f970e886488b428a65e155bdcbd80eb5a200d21d727",
        url="https://pypi.org/packages/08/b9/f5b4f79a558592f105fd2821d034f0e5151c101f2ad57e5a2e30462bacab/pgzip-0.3.1-py3-none-any.whl",
    )

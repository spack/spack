# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFileMagic(PythonPackage):
    """This library is a Python ctypes interface to libmagic"""

    homepage = "https://pypi.org/project/file-magic/"
    pypi = "file-magic/file-magic-0.4.1.tar.gz"

    version(
        "0.4.1",
        sha256="cb9496a1656baf75cadd771479f63b53081095e968d0be72b9b7a7ed538e4fb8",
        url="https://pypi.org/packages/bd/13/de7c05b7b64f4e41cca7385642884490e2fa704dc1e695d1429119caa9c2/file_magic-0.4.1-py3-none-any.whl",
    )

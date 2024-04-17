# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPastel(PythonPackage):
    """Bring colors to your terminal."""

    homepage = "https://github.com/sdispater/pastel"
    pypi = "pastel/pastel-0.2.1.tar.gz"

    license("MIT")

    version(
        "0.2.1",
        sha256="4349225fcdf6c2bb34d483e523475de5bb04a5c10ef711263452cb37d7dd4364",
        url="https://pypi.org/packages/aa/18/a8444036c6dd65ba3624c63b734d3ba95ba63ace513078e1580590075d21/pastel-0.2.1-py2.py3-none-any.whl",
    )

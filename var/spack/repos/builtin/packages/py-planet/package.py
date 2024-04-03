# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPlanet(PythonPackage):
    """Python client library and CLI for Planet's public API"""

    homepage = "https://github.com/planetlabs/planet-client-python"
    pypi = "planet/planet-1.4.6.tar.gz"

    license("Apache-2.0")

    version(
        "1.4.6",
        sha256="63079d4c196aee1a520ca7f3cf99227dd021fbb0fd0d9567f8fc86fb76f9660e",
        url="https://pypi.org/packages/d0/89/6d342925871f4fe875351c582ebb0346baf3572ada813b63c281b3c20427/planet-1.4.6-py2.py3-none-any.whl",
    )

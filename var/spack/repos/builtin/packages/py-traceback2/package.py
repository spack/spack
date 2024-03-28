# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTraceback2(PythonPackage):
    """Backports of the traceback module"""

    homepage = "https://github.com/testing-cabal/traceback2"
    pypi = "traceback2/traceback2-1.4.0.tar.gz"

    version(
        "1.4.0",
        sha256="8253cebec4b19094d67cc5ed5af99bf1dba1285292226e98a31929f87a5d6b23",
        url="https://pypi.org/packages/17/0a/6ac05a3723017a967193456a2efa0aa9ac4b51456891af1e2353bb9de21e/traceback2-1.4.0-py2.py3-none-any.whl",
    )

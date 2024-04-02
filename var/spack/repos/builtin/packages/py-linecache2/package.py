# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyLinecache2(PythonPackage):
    """Backports of the linecache module"""

    homepage = "https://github.com/testing-cabal/linecache2"
    pypi = "linecache2/linecache2-1.0.0.tar.gz"

    version(
        "1.0.0",
        sha256="e78be9c0a0dfcbac712fe04fbf92b96cddae80b1b842f24248214c8496f006ef",
        url="https://pypi.org/packages/c7/a3/c5da2a44c85bfbb6eebcfc1dde24933f8704441b98fdde6528f4831757a6/linecache2-1.0.0-py2.py3-none-any.whl",
    )

# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPrwlock(PythonPackage):
    """Native process-shared rwlock support for Python"""

    homepage = "https://github.com/renatolfc/prwlock"
    pypi = "prwlock/prwlock-0.4.1.tar.gz"

    license("MIT")

    version(
        "0.4.1",
        sha256="a12339f729f69985581e68628336446f8abf6c99aadc9fde622ed201024dd37d",
        url="https://pypi.org/packages/4a/d1/de4285f150a66ed3fb281560c0d249fe38356730f5ecbaf2847696e3bac1/prwlock-0.4.1-py3-none-any.whl",
    )

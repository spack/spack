# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGraphlibBackport(PythonPackage):
    """Backport of the Python 3.9 graphlib module for Python 3.6+."""

    homepage = "https://github.com/mariushelf/graphlib_backport"
    pypi = "graphlib_backport/graphlib_backport-1.0.3.tar.gz"

    version(
        "1.0.3",
        sha256="24246967b9e7e6a91550bc770e6169585d35aa32790258579a8a3899a8c18fde",
        url="https://pypi.org/packages/b0/2a/d77491343f72546943dd79974133a5261b9bc12a80806c34f51a058c0732/graphlib_backport-1.0.3-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@:3")

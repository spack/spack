# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPkgutilResolveName(PythonPackage):
    """Resolve a name to an object. A backport of Python 3.9 `pkgutil.resolve_name`"""

    homepage = "https://github.com/graingert/pkgutil-resolve-name"
    pypi = "pkgutil_resolve_name/pkgutil_resolve_name-1.3.10.tar.gz"

    version(
        "1.3.10",
        sha256="ca27cc078d25c5ad71a9de0a7a330146c4e014c2462d9af19c6b828280649c5e",
        url="https://pypi.org/packages/c9/5c/3d4882ba113fd55bdba9326c1e4c62a15e674a2501de4869e6bd6301f87e/pkgutil_resolve_name-1.3.10-py3-none-any.whl",
    )

# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyLockfile(PythonPackage):
    """The lockfile package exports a LockFile class which provides a
    simple API for locking files. Unlike the Windows msvcrt.locking
    function, the fcntl.lockf and flock functions, and the
    deprecated posixfile module, the API is identical across both
    Unix (including Linux and Mac) and Windows platforms. The lock
    mechanism relies on the atomic nature of the link (on Unix) and
    mkdir (on Windows) system calls. An implementation based on
    SQLite is also provided, more as a demonstration of the
    possibilities it provides than as production-quality code.
    """

    pypi = "lockfile/lockfile-0.10.2.tar.gz"
    homepage = "https://launchpad.net/pylockfile"

    license("MIT")

    version(
        "0.12.2",
        sha256="6c3cb24f344923d30b2785d5ad75182c8ea7ac1b6171b08657258ec7429d50fa",
        url="https://pypi.org/packages/c8/22/9460e311f340cb62d26a38c419b1381b8593b0bb6b5d1f056938b086d362/lockfile-0.12.2-py2.py3-none-any.whl",
    )
    version(
        "0.10.2",
        sha256="81ee2d4b0923a2ee3e51b93af0db82efa3f049c7435a00549f9a3ba22cf70cbf",
        url="https://pypi.org/packages/14/00/cf7b269d28ba8919b64a2139f65c4ecc853dec61992cd542c202ed91a9e6/lockfile-0.10.2-py2-none-any.whl",
    )

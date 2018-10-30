# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


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
    homepage = "https://pypi.python.org/pypi/lockfile"
    url      = "https://pypi.io/packages/source/l/lockfile/lockfile-0.10.2.tar.gz"

    version('0.10.2', '1aa6175a6d57f082cd12e7ac6102ab15')

    depends_on("py-setuptools", type='build')

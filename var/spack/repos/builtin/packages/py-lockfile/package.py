##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
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
    url      = "https://pypi.python.org/packages/source/l/lockfile/lockfile-0.10.2.tar.gz"

    version('0.10.2', '1aa6175a6d57f082cd12e7ac6102ab15')

    depends_on("py-setuptools", type='build')

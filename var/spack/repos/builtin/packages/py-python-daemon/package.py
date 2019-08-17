# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPythonDaemon(PythonPackage):
    """Library to implement a well-behaved Unix daemon process.

       This library implements the well-behaved daemon specification of
       PEP Standard daemon process.

       A well-behaved Unix daemon process is tricky to get right, but the
       required steps are much the same for every daemon program. A
       DaemonContext instance holds the behaviour and configured process
       environment for the program; use the instance as a context manager
       to enter a daemon state.
    """
    homepage = "https://pypi.python.org/pypi/python-daemon/"
    url      = "https://pypi.io/packages/source/p/python-daemon/python-daemon-2.0.5.tar.gz"

    version('2.0.5', '73e7f49f525c51fa4a995aea4d80de41')

    depends_on("py-setuptools", type='build')
    depends_on("py-lockfile", type=('build', 'run'))

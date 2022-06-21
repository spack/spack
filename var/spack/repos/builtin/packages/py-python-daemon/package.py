# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


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
    pypi = "python-daemon/python-daemon-2.0.5.tar.gz"

    version('2.3.0', sha256='bda993f1623b1197699716d68d983bb580043cf2b8a66a01274d9b8297b0aeaf')
    version('2.0.5', sha256='afde4fa433d94d007206ee31a0941d55b5eb232a5422b670aad628547b46bf68')

    depends_on("py-setuptools", type=('build', 'run'))
    depends_on("py-lockfile", type=('build', 'run'))
    depends_on("py-lockfile@0.10:", type=('build', 'run'), when='@2.3.0:')
    depends_on("py-docutils", type='build')
    depends_on("py-twine", type='build')

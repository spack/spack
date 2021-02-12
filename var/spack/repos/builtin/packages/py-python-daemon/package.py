# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
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
    pypi = "python-daemon/python-daemon-2.0.5.tar.gz"

    version('2.2.4', sha256='57c84f50a04d7825515e4dbf3a31c70cc44414394a71608dee6cfde469e81766')
    version('2.2.3', sha256='affeca9e5adfce2666a63890af9d6aff79f670f7511899edaddca7f96593cc25')
    version('2.2.2', sha256='d8732192a408cc87f90b14efb9347237782a88f9dda52a5797e88da219069117')
    version('2.2.1', sha256='d7ee3267278900a99b1aade80d351fdf0dbe2a517ca184a409f9b2e2121552b8')
    version('2.2.0', sha256='aca149ebf7e73f10cd554b2df5c95295d49add8666348eff6195053ec307728c')
    version('2.1.2', sha256='261c859be5c12ae7d4286dc6951e87e9e1a70a882a8b41fd926efc1ec4214f73')
    version('2.1.1', sha256='58a8c187ee37c3a28913bef00f83240c9ecd4a59dce09a24d92f5c941606689f')
    version('2.1.0', sha256='ae30f6d4d7399665317f90d986686cf455a1b3e61e3c042cc00a39a34e3b4825')
    version('2.0.6', sha256='1730b8e80773379857bf4a792ccccea2cda05c151fbee986b909ceddafa27309')
    version('2.0.5', sha256='afde4fa433d94d007206ee31a0941d55b5eb232a5422b670aad628547b46bf68')

    depends_on("py-setuptools", type='build')
    depends_on("py-lockfile", type=('build', 'run'))

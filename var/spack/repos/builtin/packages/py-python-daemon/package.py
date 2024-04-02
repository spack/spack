# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
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

    license("GPL-3.0-or-later")

    version(
        "2.3.1",
        sha256="4e3bf67784c78aaa55ec001a2f832b464a54c5f9c89c11b311e2416a8c247431",
        url="https://pypi.org/packages/aa/b0/bc79d8ff019c2583d839e0143b1f91eafd4cfe92f86fb9d378a515dfb612/python_daemon-2.3.1-py2.py3-none-any.whl",
    )
    version(
        "2.3.0",
        sha256="191c7b67b8f7aac58849abf54e19fe1957ef7290c914210455673028ad454989",
        url="https://pypi.org/packages/b1/cc/2ab0d910548de45eaaa50d0372387951d9005c356a44c6858db12dc6b2b7/python_daemon-2.3.0-py2.py3-none-any.whl",
    )
    version(
        "2.0.5",
        sha256="db316a0fcf54b9702caf6ca619b76be25d53f5ee0781baff0bb9e2e0355faf24",
        url="https://pypi.org/packages/5b/90/b55062dbce72c24ba1c1655b07974b300a66f352800152e6ed21f29b7dc4/python_daemon-2.0.5-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-docutils", when="@2.2.1:")
        depends_on("py-lockfile@0.10:", when="@2.2.1:")
        depends_on("py-setuptools", when="@2.2.1:3.0.0")

# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySortedcontainers(PythonPackage):
    """Sorted Containers is an Apache2 licensed sorted collections library,
    written in pure-Python, and fast as C-extensions."""

    homepage = "http://www.grantjenks.com/docs/sortedcontainers/"
    pypi = "sortedcontainers/sortedcontainers-2.1.0.tar.gz"

    license("Apache-2.0")

    version(
        "2.4.0",
        sha256="a163dcaede0f1c021485e957a39245190e74249897e2ae4b2aa38595db237ee0",
        url="https://pypi.org/packages/32/46/9cb0e58b2deb7f82b84065f37f3bffeb12413f947f9388e4cac22c4621ce/sortedcontainers-2.4.0-py2.py3-none-any.whl",
    )
    version(
        "2.1.0",
        sha256="d9e96492dd51fae31e60837736b38fe42a187b5404c16606ff7ee7cd582d4c60",
        url="https://pypi.org/packages/13/f3/cf85f7c3a2dbd1a515d51e1f1676d971abe41bba6f4ab5443240d9a78e5b/sortedcontainers-2.1.0-py2.py3-none-any.whl",
    )

# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyNetaddr(PythonPackage):
    """A system-independent network address manipulation library for Python"""

    homepage = "https://netaddr.readthedocs.io/en/latest/"
    pypi = "netaddr/netaddr-0.8.0.tar.gz"

    maintainers("haampie")

    license("BSD-3-Clause")

    version(
        "0.8.0",
        sha256="9666d0232c32d2656e5e5f8d735f58fd6c7457ce52fc21c98d45f2af78f990ac",
        url="https://pypi.org/packages/ff/cd/9cdfea8fc45c56680b798db6a55fa60a22e2d3d3ccf54fc729d083b50ce4/netaddr-0.8.0-py2.py3-none-any.whl",
    )

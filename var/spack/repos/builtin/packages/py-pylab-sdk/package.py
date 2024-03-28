# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPylabSdk(PythonPackage):
    """A development kit that collects simple utilities."""

    homepage = "https://github.com/PyLabCo/pylab-sdk"
    pypi = "pylab-sdk/pylab-sdk-1.3.2.tar.gz"

    license("MIT")

    version(
        "1.3.2",
        sha256="a6784769f3cb4626f732ff22f0ad88a470c4ab294e1c52f82f5167bc27f9be46",
        url="https://pypi.org/packages/ed/67/9a73c2b0144314da579e8c61ab8beaff55905d68caed86e5de2460505329/pylab_sdk-1.3.2-py3-none-any.whl",
    )

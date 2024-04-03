# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPythonCertifiWin32(PythonPackage):
    """This package patches certifi at runtime to also include certificates from the
    windows certificate store."""

    homepage = "https://gitlab.com/alelec/python-certifi-win32"
    git = "https://gitlab.com/alelec/python-certifi-win32.git"

    license("BSD-2-Clause")

    # Tarball missing version information, need to use git checkout
    version(
        "1.6",
        sha256="a1656aecc71eff60b43ff319290e42523574a00a101801c664933fa164c021a4",
        url="https://pypi.org/packages/c1/43/916ef701ae481e04ed87af26fd54fa3906d44239f32d7f43be2fcbf54896/python_certifi_win32-1.6-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-certifi")
        depends_on("py-setuptools-scm", when="@1.4:")
        depends_on("py-wrapt@1.10.4:")

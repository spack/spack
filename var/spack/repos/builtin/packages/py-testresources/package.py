# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTestresources(PythonPackage):
    """Testresources, a pyunit extension for managing expensive test resources."""

    homepage = "https://launchpad.net/testresources"
    pypi = "testresources/testresources-2.0.1.tar.gz"

    license("Apache-2.0")

    version(
        "2.0.1",
        sha256="67a361c3a2412231963b91ab04192209aa91a1aa052f0ab87245dbea889d1282",
        url="https://pypi.org/packages/45/4d/79a9a1f71de22fbc6c6433ac135f68d005de72fbe73e2137d2e77da9252c/testresources-2.0.1-py2.py3-none-any.whl",
    )

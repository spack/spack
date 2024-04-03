# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPythonSubunit(PythonPackage):
    """Python implementation of subunit test streaming protocol."""

    homepage = "https://launchpad.net/subunit"
    pypi = "python-subunit/python-subunit-1.3.0.tar.gz"

    license("MIT")

    version(
        "1.3.0",
        sha256="693f1bcb4fe4bd53438ee0b524c8280143e538d663fb92fb66bad05f744a0132",
        url="https://pypi.org/packages/ee/3a/b8a93e1f5b9a9f7e0a7630146f1c62878b6949ac5e4bac6ae2ae13fa9f83/python_subunit-1.3.0-py2.py3-none-any.whl",
    )

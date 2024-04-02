# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCurrent(PythonPackage):
    """Current module relative paths and imports"""

    homepage = "https://github.com/xflr6/current"
    pypi = "current/current-0.3.1.zip"

    license("Condor-1.1")

    version(
        "0.3.1",
        sha256="5b1e2ddabd3de44be215b66abc840061787d9e82a6f1d332e3cf23786652f12a",
        url="https://pypi.org/packages/79/c3/40a7568d3ab53b70d40b5a169b425932b8c84dd6244d5ede629a329fa322/current-0.3.1-py2.py3-none-any.whl",
    )

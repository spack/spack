# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySlicer(PythonPackage):
    """slicer wraps tensor-like objects and provides a uniform slicing interface via __getitem__"""

    homepage = "https://github.com/interpretml/slicer"
    pypi = "slicer/slicer-0.0.7.tar.gz"

    version(
        "0.0.7",
        sha256="0b94faa5251c0f23782c03f7b7eedda91d80144059645f452c4bc80fab875976",
        url="https://pypi.org/packages/78/c2/b3f55dfdb8af9812fdb9baf70cacf3b9e82e505b2bd4324d588888b81202/slicer-0.0.7-py3-none-any.whl",
    )

# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAniso8601(PythonPackage):
    """A library for parsing ISO 8601 strings."""

    homepage = "https://bitbucket.org/nielsenb/aniso8601"
    pypi = "aniso8601/aniso8601-9.0.1.tar.gz"

    license("BSD-3-Clause")

    version(
        "9.0.1",
        sha256="1d2b7ef82963909e93c4f24ce48d4de9e66009a21bf1c1e1c85bdd0812fe412f",
        url="https://pypi.org/packages/e3/04/e97c12dc034791d7b504860acfcdd2963fa21ae61eaca1c9d31245f812c3/aniso8601-9.0.1-py2.py3-none-any.whl",
    )
    version(
        "7.0.0",
        sha256="d10a4bf949f619f719b227ef5386e31f49a2b6d453004b21f02661ccc8670c7b",
        url="https://pypi.org/packages/45/a4/b4fcadbdab46c2ec2d2f6f8b4ab3f64fd0040789ac7f065eba82119cd602/aniso8601-7.0.0-py2.py3-none-any.whl",
    )

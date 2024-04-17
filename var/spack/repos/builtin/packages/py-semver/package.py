# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySemver(PythonPackage):
    """A Python module for semantic versioning.
    Simplifies comparing versions."""

    homepage = "https://semver.org/"
    pypi = "semver/semver-2.8.1.tar.gz"

    license("BSD-3-Clause")

    version(
        "3.0.1",
        sha256="2a23844ba1647362c7490fe3995a86e097bb590d16f0f32dfc383008f19e4cdf",
        url="https://pypi.org/packages/d4/5d/f2b4fe45886238c405ad177ca43911cb1459d08003004da5c27495eb4216/semver-3.0.1-py3-none-any.whl",
    )
    version(
        "2.8.1",
        sha256="41c9aa26c67dc16c54be13074c352ab666bce1fa219c7110e8f03374cd4206b0",
        url="https://pypi.org/packages/21/18/a0de8cda637ba3efee1b3617ded00601507ce15bd70a39399740e0fd415f/semver-2.8.1-py2.py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("python@3.7:", when="@3:")

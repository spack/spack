# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFprettify(PythonPackage):
    """fprettify is an auto-formatter for modern Fortran code (Fortran 90
    and later) that imposes strict whitespace formatting, written in
    Python."""

    homepage = "https://github.com/pseewald/fprettify"
    pypi = "fprettify/fprettify-0.3.6.tar.gz"

    version(
        "0.3.7",
        sha256="56f0a64c43dc47134ce32af2e5da8cd7a1584897be29d19289ec5d87510d1daf",
        url="https://pypi.org/packages/52/13/2c32d63574e116f8c933f56315df9135bf2fae7a88e9e7c6c4d37f48f4ef/fprettify-0.3.7-py3-none-any.whl",
    )
    version(
        "0.3.6",
        sha256="2190fb4f84785245d01a2945d822113137c396b1db82b7ee93fbbfbf19043f0b",
        url="https://pypi.org/packages/8a/da/0f24541c9f20f5494be76bc9300f01c391ff219f62a4a628df540a96466e/fprettify-0.3.6-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("py-configargparse", when="@0.3.4:")

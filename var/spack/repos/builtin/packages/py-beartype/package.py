# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBeartype(PythonPackage):
    """Unbearably fast near-real-time hybrid runtime-static type-checking in pure Python."""

    homepage = "https://beartype.readthedocs.io/"
    pypi = "beartype/beartype-0.15.0.tar.gz"

    license("MIT")

    version(
        "0.16.2",
        sha256="72d133615fe674affc8c49365dd24dfe2260552b9a8a2b7193cdd48021527782",
        url="https://pypi.org/packages/29/83/ed78ed7304e29741dee2d3bfd08c99b133e0c8cb600b8ff66cdf66e2706a/beartype-0.16.2-py3-none-any.whl",
    )
    version(
        "0.15.0",
        sha256="52cd2edea72fdd84e4e7f8011a9e3007bf0125c3d6d7219e937b9d8868169177",
        url="https://pypi.org/packages/6f/e7/9220de010e015fdfb7ce22e7d9a846bfcd6e5d686c4fc555fa76a22846ba/beartype-0.15.0-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("python@3.8:", when="@0.15:")

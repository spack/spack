# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBiobbIo(PythonPackage):
    """Biobb_io is the Biobb module collection to fetch data to be
    consumed by the rest of the Biobb building blocks"""

    pypi = "biobb_io/biobb_io-4.1.0.tar.gz"

    maintainers("d-beltran")

    # Versions
    version(
        "4.1.0",
        sha256="4ea494e1cbd0f4d2d5f17a8e92b81c73efbf2a25b3b34a1eb86053edf28e482f",
        url="https://pypi.org/packages/f9/d7/35ab091c2db4161002c5cf6f9de3362c813bfc0a492e8bedd0d455097df1/biobb_io-4.1.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.8:", when="@4.1:")
        depends_on("py-biobb-common@4.1:", when="@4.1:")

    # Dependencies

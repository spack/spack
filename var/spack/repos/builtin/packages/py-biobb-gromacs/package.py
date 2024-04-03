# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBiobbGromacs(PythonPackage):
    """Biobb_gromacs is the Biobb module collection to perform
    molecular dynamics simulations using the GROMACS MD suite"""

    pypi = "biobb_gromacs/biobb_gromacs-4.1.1.tar.gz"

    maintainers("d-beltran")

    # Versions
    version(
        "4.1.1",
        sha256="698f0bdb6f6f5c896513b47669d2b2c6f6b7c0c753039df61a82fb1ca57c2f80",
        url="https://pypi.org/packages/83/29/ba77b856d70014284b072f30499704544fff363802a87e370306e0076e2d/biobb_gromacs-4.1.1-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.8:", when="@4.1:")
        depends_on("py-biobb-common@4.1:", when="@4.1:")

    # Dependencies

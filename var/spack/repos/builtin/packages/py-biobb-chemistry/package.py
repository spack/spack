# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBiobbChemistry(PythonPackage):
    """Biobb module collection to perform chemistry over molecular dynamics simulations."""

    homepage = "https://biobb-chemistry.readthedocs.io"
    pypi = "biobb_chemistry/biobb_chemistry-4.1.0.tar.gz"

    maintainers("w8jcik")

    version("4.1.0", sha256="0c0d118c7dbc6733e8a647b2c362703f03043d923d4087182b4f7cb819fb6776")

    depends_on("py-biobb-common@4.1.0", type=("build", "run"))

    depends_on("py-setuptools", type="build")

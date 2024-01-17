# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBiobbAnalysis(PythonPackage):
    """Biobb module collection to perform analysis of molecular dynamics simulations."""

    homepage = "https://biobb-analysis.readthedocs.io"
    pypi = "biobb_analysis/biobb_analysis-4.1.0.tar.gz"

    maintainers("w8jcik")

    version("4.1.0", sha256="b4f0637f5f823c218ba4e066c5d7eb3288c2a9ee91fc72e9211f689e1d5c2a58")

    depends_on("py-biobb-common@4.1.0", type=("build", "run"))

    depends_on("py-setuptools", type="build")

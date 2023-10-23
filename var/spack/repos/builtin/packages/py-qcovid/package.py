# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyQcovid(PythonPackage):
    """QC pipelines for sars-cov-2 sequence+consensus submitted to the ENA"""

    homepage = "https://github.com/iqbal-lab-org/QCovid"
    url = "https://github.com/iqbal-lab-org/QCovid"
    git="https://github.com/iqbal-lab-org/QCovid"

    version("master", branch="master")

    depends_on("py-setuptools", type="build")
    depends_on("py-pysam")
    depends_on("minimap2")
    depends_on("py-sqlalchemy@1.3.20:")

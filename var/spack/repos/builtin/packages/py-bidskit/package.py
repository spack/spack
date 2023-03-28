# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBidskit(PythonPackage):
    """Tools for DICOM to BIDS conversion."""

    homepage = "https://github.com/jmtyszka/bidskit"
    pypi = "bidskit/bidskit-2022.10.13.tar.gz"

    version(
        "2022.10.13", sha256="576b92cef187032c73f64e2e6a5b0be0c06771442048a33c55e224b3df0aae3a"
    )

    depends_on("python@3.7:3", type=("build", "run"))
    depends_on("py-setuptools", type="build")

    depends_on("py-pydicom@2.2:", type=("build", "run"))
    depends_on("py-pybids@0.15:", type=("build", "run"))
    depends_on("py-numpy@1.21:", type=("build", "run"))

    # version requirement comes from error message when using bidskit
    depends_on("dcm2niix@1.0.20220720:", type=("build", "run"))

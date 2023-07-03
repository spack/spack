# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyRseqc(PythonPackage):
    """RSeQC package provides a number of useful modules that can
    comprehensively evaluate high throughput sequence data especially RNA-seq
    data."""

    homepage = "http://rseqc.sourceforge.net"
    pypi = "RSeQC/RSeQC-2.6.4.tar.gz"

    version("3.0.1", sha256="d5f4cb2c24a7348929f5c4947d84c5869e8cd2cba5ba5248d991ebb37c4c6b3d")

    depends_on("python@3.5:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-nose@0.10.4:", type="build")
    depends_on("py-cython@0.17:", type=("build", "run"))
    depends_on("py-bx-python", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-pysam", type=("build", "run"))
    depends_on("py-pybigwig", type=("build", "run"))
    depends_on("r", type="run")

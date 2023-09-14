# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RTiff(RPackage):
    """Read and write TIFF images.

    This package provides an easy and simple way to read, write and display
    bitmap images stored in the TIFF format. It can read and write both files
    and in-memory raw vectors."""

    cran = "tiff"

    version("0.1-11", sha256="b8c3ea15114d972f8140541c7b01f5ce2e5322af1f63c1a083aaf766fd3eec75")
    version("0.1-10", sha256="535154e89e85e14fe697469d2c59826a44c7937e7eca2eaca1aee6b0fe320afe")
    version("0.1-6", sha256="623bd9c16a426df7e6056738c5d91da86ea9b49df375eea6b5127e4e458dc4fb")
    version("0.1-5", sha256="9514e6a9926fcddc29ce1dd12b1072ad8265900373f738de687ef4a1f9124e2b")

    depends_on("r@2.9.0:", type=("build", "run"))
    depends_on("libtiff")
    depends_on("jpeg")

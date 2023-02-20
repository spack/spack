# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RNnls(RPackage):
    """The Lawson-Hanson algorithm for non-negative least squares (NNLS).

    An R interface to the Lawson-Hanson implementation of an algorithm for
    non-negative least squares (NNLS). Also allows the combination of
    non-negative and non-positive constraints."""

    cran = "nnls"

    version("1.4", sha256="0e5d77abae12bc50639d34354f96a8e079408c9d7138a360743b73bd7bce6c1f")

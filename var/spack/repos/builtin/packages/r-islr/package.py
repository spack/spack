# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RIslr(RPackage):
    """ISLR: Data for an Introduction to Statistical Learning with Applications
    in R

    We provide the collection of data-sets used in the book 'An Introduction to
    Statistical Learning with Applications in R'."""

    homepage = "https://cloud.r-project.org/package=ISLR"
    url      = "https://cloud.r-project.org/src/contrib/ISLR_1.2.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/ISLR"

    version('1.2', sha256='b00f7a06d2fb646917e629cc2dbdab71c7de3eb17a8a4d06849901a299f1caad')

    depends_on('r@2.10:', type=('build', 'run'))

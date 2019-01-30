# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RAde4(RPackage):
    """Analysis of Ecological Data : Exploratory and Euclidean Methods in
    Environmental Sciences"""

    homepage = "http://pbil.univ-lyon1.fr/ADE-4"
    url      = "https://cran.r-project.org/src/contrib/ade4_1.7-6.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/ade4"

    version('1.7-6', '63401ca369677538c96c3d7b75b3f4a1')

    depends_on('r@2.10:')

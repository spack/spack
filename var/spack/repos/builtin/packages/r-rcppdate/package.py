# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RRcppdate(RPackage):
    """'date' C++ Header Library for Date and Time Functionality

    'date' is a C++ header library offering extensive date and time
    functionality for the C++11, C++14 and C++17 standards written by Howard
    Hinnant and released under the MIT license. A slightly modified version has
    been accepted (along with 'tz.h') as part of C++20. This package regroups
    all header files from the upstream repository by Howard Hinnant so that
    other R packages can use them in their C++ code. At present, few of the
    types have explicit 'Rcpp' wrapper though these may be added as needed."""

    homepage = "https://github.com/eddelbuettel/rcppdate"
    url      = "https://cloud.r-project.org/src/contrib/RcppDate_0.0.1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/RcppDate"

    version('0.0.2', sha256='d494e691f28014967094fdb8779d6b2ff831f13f7e8193241e0313cc409b84b0')
    version('0.0.1', sha256='117721fc677dfb4209200a7ff894fbbb8ee1b652d01b3878b11c3253733b4a5f')

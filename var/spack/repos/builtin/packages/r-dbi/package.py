# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RDbi(RPackage):
    """A database interface definition for communication between R and
    relational database management systems. All classes in this package are
    virtual and need to be extended by the various R/DBMS implementations."""

    homepage = "http://rstats-db.github.io/DBI"
    url      = "https://cran.rstudio.com/src/contrib/DBI_0.7.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/DBI"
    version('0.4-1', 'c7ee8f1c5037c2284e99c62698d0f087')
    version('0.7', '66065dd687d758b72d638adb6a8cab2e')

# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RNp(RPackage):
    """This package provides a variety of nonparametric (and semiparametric)
    kernel methods that seamlessly handle a mix of continuous, unordered, and
    ordered factor data types. We would like to gratefully acknowledge support
    from the Natural Sciences and Engineering Research Council of Canada
    (NSERC:www.nserc.ca), the Social Sciences and Humanities Research Council
    of Canada (SSHRC:www.sshrc.ca), and the Shared Hierarchical Academic
    Research Computing Network (SHARCNET:www.sharcnet.ca)."""

    homepage = "https://github.com/JeffreyRacine/R-Package-np/"
    url      = "https://cran.r-project.org/src/contrib/np_0.60-2.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/np"

    version('0.60-2', 'e094d52ddff7280272b41e6cb2c74389')

    depends_on('r-boot', type=('build', 'run'))
    depends_on('r-cubature', type=('build', 'run'))

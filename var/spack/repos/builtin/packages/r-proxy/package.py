# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RProxy(RPackage):
    """Provides an extensible framework for the efficient calculation of
       auto- and cross-proximities, along with implementations of the most
       popular ones."""

    homepage = "https://cran.r-project.org/package=proxy"
    url      = "https://cran.rstudio.com/src/contrib/proxy_0.4-19.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/proxy"
    version('0.4-19', '279a01a1cc12ed50208c98196d78a5d7')

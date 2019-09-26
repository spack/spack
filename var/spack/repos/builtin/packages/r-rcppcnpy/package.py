# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RRcppcnpy(RPackage):
    """Rcpp bindings for NumPy files."""

    homepage = "https://github.com/eddelbuettel/rcppcnpy"
    url      = "https://cloud.r-project.org/src/contrib/RcppCNPy_0.2.9.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/RcppCNPy"

    version('0.2.10', sha256='77d6fbc86520a08da40d44c0b82767099f8f719ca95870d91efff1a9cab1ab9c')
    version('0.2.9', '7f63354d15928b6716830c2975b3baf0')

    depends_on('r@3.1.0:', type=('build', 'run'))
    depends_on('r-rcpp', type=('build', 'run'))

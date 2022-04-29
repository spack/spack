# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.pkgkit import *


class RTriebeard(RPackage):
    """'Radix' Trees in 'Rcpp'.

    'Radix trees', or 'tries', are key-value data structures optimised for
    efficient lookups, similar in purpose to hash tables. 'triebeard' provides
    an implementation of 'radix trees' for use in R programming and in
    developing packages with 'Rcpp'."""

    cran = "triebeard"

    version('0.3.0', sha256='bf1dd6209cea1aab24e21a85375ca473ad11c2eff400d65c6202c0fb4ef91ec3')

    depends_on('r-rcpp', type=('build', 'run'))

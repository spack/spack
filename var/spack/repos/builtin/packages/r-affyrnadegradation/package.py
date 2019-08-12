# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RAffyrnadegradation(RPackage):
    """The package helps with the assessment and correction of
    RNA degradation effects in Affymetrix 3' expression arrays.
    The parameter d gives a robust and accurate measure of RNA
    integrity. The correction removes the probe positional bias,
    and thus improves comparability of samples that are affected
    by RNA degradation."""

    homepage = "https://www.bioconductor.org/packages/AffyRNADegradation/"
    git      = "https://git.bioconductor.org/packages/AffyRNADegradation.git"

    version('1.22.0', commit='0fa78f8286494711a239ded0ba587b0de47c15d3')

    depends_on('r@3.4.0:3.4.9', when='@1.22.0')
    depends_on('r-affy', type=('build', 'run'))

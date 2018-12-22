# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RQvalue(RPackage):
    """This package takes a list of p-values resulting from the
    simultaneous testing of many hypotheses and estimates their
    q-values and local FDR values. The q-value of a test measures
    the proportion of false positives incurred (called the false
    discovery rate) when that particular test is called significant.
    The local FDR measures the posterior probability the null
    hypothesis is true given the test's p-value. Various plots are
    automatically generated, allowing one to make sensible
    significance cut-offs. Several mathematical results have
    recently been shown on the conservative accuracy of the
    estimated q-values from this software. The software can be
    applied to problems in genomics, brain imaging, astrophysics,
    and data mining."""

    homepage = "https://www.bioconductor.org/packages/qvalue/"
    git      = "https://git.bioconductor.org/packages/qvalue.git"

    version('2.12.0', commit='7df64ebfcbe69dcbf8b88cb6ef0068bf16979673')
    version('2.8.0', commit='c7bf3315619d42d800f57a36670c25a7495ded72')

    depends_on('r-ggplot2', type=('build', 'run'))
    depends_on('r-reshape2', type=('build', 'run'))
    depends_on('r@3.4.0:3.4.9', when='@2.8.0', type=('build', 'run'))
    depends_on('r@3.5.0:3.5.9', when='@2.12.0', type=('build', 'run'))

# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RTximportdata(RPackage):
    """Import and summarize transcript-level estimates for transcript- and
    gene-level analysis.

    Imports transcript-level abundance, estimated counts and transcript
    lengths, and summarizes into matrices for use with downstream gene-level
    analysis packages. Average transcript length, weighted by sample-specific
    transcript abundance estimates, is provided as a matrix which can be used
    as an offset for different expression of gene-level counts."""

    bioc = "tximportData"

    version('1.22.0', commit='c576b18e43985baf8beab327cbc54afe8324659c')
    version('1.18.0', commit='24945f8dd1e4e441ad5145fb7a37a1630912f929')

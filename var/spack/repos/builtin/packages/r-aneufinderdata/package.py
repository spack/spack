# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RAneufinderdata(RPackage):
    """Whole-genome single cell sequencing data for demonstration
    purposes in the AneuFinder package."""

    homepage = "https://www.bioconductor.org/packages/AneuFinderData/"
    git      = "https://git.bioconductor.org/packages/AneuFinderData.git"

    version('1.4.0', commit='55c8807ee4a37a2eb6d0defafaf843f980b22c40')

    depends_on('r@3.4.0:3.4.9', when='@1.4.0')

# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RMatr(RPackage):
    """Package matR (Metagenomics Analysis Tools for R) is an analysis
    client for the MG-RAST metagenome annotation engine, part of the US
    Department of Energy (DOE) Systems Biology Knowledge Base (KBase).
    Customized analysis and visualization tools securely access remote
    data and metadata within the popular open source R language and
    environment for statistical computing."""

    homepage = "https://github.com/MG-RAST/matR"
    url      = "https://cran.r-project.org/src/contrib/Archive/matR/matR_0.9.tar.gz"

    version('0.9', 'e2be8734009f5c5b9c1f6b677a77220a')

    depends_on('r-mgraster', type=('build', 'run'))
    depends_on('r-biom-utils', type=('build', 'run'))

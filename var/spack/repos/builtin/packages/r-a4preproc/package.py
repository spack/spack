# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RA4preproc(RPackage):
    """Automated Affymetrix Array Analysis Preprocessing Package."""

    homepage = "https://www.bioconductor.org/packages/a4Preproc/"
    git      = "https://git.bioconductor.org/packages/a4Preproc.git"

    version('1.24.0', commit='651014b8102807aea4f1274e34e083e70b5e7ee7')

    depends_on('r@3.4.0:3.4.9', when='@1.24.0')
    depends_on('r-annotationdbi', type=('build', 'run'))

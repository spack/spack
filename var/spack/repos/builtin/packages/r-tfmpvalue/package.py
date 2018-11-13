# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RTfmpvalue(RPackage):
    """In putative Transcription Factor Binding Sites (TFBSs) identification
       from sequence/alignments, we are interested in the significance of
       certain match score. TFMPvalue provides the accurate calculation of
       P-value with score threshold for Position Weight Matrices, or the score
       with given P-value. This package is an interface to code originally
       made available by Helene Touzet and Jean-Stephane Varre, 2007,
       Algorithms Mol Biol:2, 15."""

    homepage = "https://github.com/ge11232002/TFMPvalue"
    url      = "https://cran.rstudio.com/src/contrib/TFMPvalue_0.0.6.tar.gz"
    list_url = "https://cran.rstudio.com/src/contrib/Archive/TFMPvalue"

    version('0.0.6', '69fdf4f9b9a0f408a5cee9ce34bea261')

    depends_on('r-rcpp@0.11.1:', type=('build', 'run'))

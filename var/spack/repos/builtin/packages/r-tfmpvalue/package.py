##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
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

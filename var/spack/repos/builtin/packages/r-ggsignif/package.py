##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
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


class RGgsignif(RPackage):
    """Enrich your 'ggplots' with group-wise comparisons. This package
    provides an easy way to indicate if two groups are significantly
    different. Commonly this is shown by a bracket on top connecting the
    groups of interest which itself is annotated with the level of
    significance (NS, *, **, ***). The package provides a single layer
    (geom_signif()) that takes the groups for comparison and the test
    (t.test(), wilcox.text() etc.) as arguments and adds the annotation
    to the plot."""

    homepage = "https://github.com/const-ae/ggsignif"
    url      = "https://cran.r-project.org/src/contrib/ggsignif_0.3.0.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/ggsignif"

    version('0.3.0', '649139aa0f9b4e713f27bccf63cb1942')

    depends_on('r-ggplot2@2.0.0:', type=('build', 'run'))

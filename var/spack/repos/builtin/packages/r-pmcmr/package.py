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


class RPmcmr(RPackage):
    """The Kruskal and Wallis one-way analysis of variance by ranks or van
       der Waerden's normal score test can be employed, if the data do not
       meet the assumptions for one-way ANOVA. Provided that significant
       differences were detected by the omnibus test, one may be interested
       in applying post-hoc tests for pairwise multiple comparisons (such as
       Nemenyi's test, Dunn's test, Conover's test, van der Waerden's test).
       Similarly, one-way ANOVA with repeated measures that is also referred
       to as ANOVA with unreplicated block design can also be conducted via
       the Friedman-Test or the Quade-test. The consequent post-hoc pairwise
       multiple comparison tests according to Nemenyi, Conover and Quade are
       also provided in this package. Finally Durbin's test for a two-way
       balanced incomplete block design (BIBD) is also given in this
       package."""

    homepage = "https://cran.r-project.org/package=PMCMR"
    url      = "https://cran.rstudio.com/src/contrib/PMCMR_4.1.tar.gz"
    list_url = "https://cran.rstudio.com/src/contrib/Archive/PMCMR"

    version('4.1', 'b9c0c4e4cb4f73ae36f45a47abae986a')

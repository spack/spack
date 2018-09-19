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


class RReportingtools(RPackage):
    """The ReportingTools software package enables users to easily
    display reports of analysis results generated from sources such
    as microarray and sequencing data. The package allows users to
    create HTML pages that may be viewed on a web browser such as
    Safari, or in other formats readable by programs such as Excel.
    Users can generate tables with sortable and filterable columns,
    make and display plots, and link table entries to other data
    sources such as NCBI or larger plots within the HTML page. Using
    the package, users can also produce a table of contents page to
    link various reports together for a particular project that can
    be viewed in a web browser. For more examples, please visit our
    site: http:// research-pub.gene.com/ReportingTools."""

    homepage = "https://bioconductor.org/packages/ReportingTools/"
    git      = "https://git.bioconductor.org/packages/ReportingTools.git"

    version('2.16.0', commit='b1aa0ea302da7f2993ce8087b1d09c11ddf03663')

    depends_on('r@3.4.0:3.4.9', when='@2.16.0')
    depends_on('r-knitr', type=('build', 'run'))
    depends_on('r-biobase', type=('build', 'run'))
    depends_on('r-hwriter', type=('build', 'run'))
    depends_on('r-category', type=('build', 'run'))
    depends_on('r-gostats', type=('build', 'run'))
    depends_on('r-limma', type=('build', 'run'))
    depends_on('r-limma', type=('build', 'run'))
    depends_on('r-lattice', type=('build', 'run'))
    depends_on('r-annotationdbi', type=('build', 'run'))
    depends_on('r-edger', type=('build', 'run'))
    depends_on('r-annotate', type=('build', 'run'))
    depends_on('r-pfam-db', type=('build', 'run'))
    depends_on('r-gseabase', type=('build', 'run'))
    depends_on('r-biocgenerics', type=('build', 'run'))
    depends_on('r-xml', type=('build', 'run'))
    depends_on('r-utils', type=('build', 'run'))
    depends_on('r-deseq2', type=('build', 'run'))
    depends_on('r-ggplot2', type=('build', 'run'))
    depends_on('r-ggbio', type=('build', 'run'))
    depends_on('r-iranges', type=('build', 'run'))

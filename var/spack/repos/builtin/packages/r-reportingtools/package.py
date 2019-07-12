# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RReportingtools(RPackage):
    """Tools for making reports in various formats

       The ReportingTools software package enables users to easily display
       reports of analysis results generated from sources such as microarray
       and sequencing data. The package allows users to create HTML pages that
       may be viewed on a web browser such as Safari, or in other formats
       readable by programs such as Excel. Users can generate tables with
       sortable and filterable columns, make and display plots, and link table
       entries to other data sources such as NCBI or larger plots within the
       HTML page. Using the package, users can also produce a table of contents
       page to link various reports together for a particular project that can
       be viewed in a web browser. For more examples, please visit our site:
       http:// research-pub.gene.com/ReportingTools."""

    homepage = "https://bioconductor.org/packages/ReportingTools"
    git      = "https://git.bioconductor.org/packages/ReportingTools.git"

    version('2.24.0', commit='d114c658affba9b682a37b4e2caf4341cf8da6cf')
    version('2.22.1', commit='dce6af6c6a1cddff077fe61368f2c13e5a0e7bab')
    version('2.20.0', commit='77e14ae13fdc16654300852dfd94e6cef58009da')
    version('2.17.3', commit='b2e379cd5b813d8ccca37ec25f0660deec943622')
    version('2.16.0', commit='b1aa0ea302da7f2993ce8087b1d09c11ddf03663')

    depends_on('r@3.6.0:3.6.9', when='@2.24.0', type=('build', 'run'))
    depends_on('r@3.5.0:3.5.9', when='@2.22.1', type=('build', 'run'))
    depends_on('r@3.5.0:3.5.9', when='@2.20.0', type=('build', 'run'))
    depends_on('r@3.4.0:3.4.9', when='@2.17.3', type=('build', 'run'))
    depends_on('r@3.4.0:3.4.9', when='@2.16.0', type=('build', 'run'))

    depends_on('r-annotate', when='@2.16.0:', type=('build', 'run'))
    depends_on('r-annotationdbi', when='@2.16.0:', type=('build', 'run'))
    depends_on('r-biobase', when='@2.16.0:', type=('build', 'run'))
    depends_on('r-biocgenerics(>=@0.1.6:', when='@2.16.0:', type=('build', 'run'))
    depends_on('r-category', when='@2.16.0:', type=('build', 'run'))
    depends_on('r-deseq2(>=@1.3.41:', when='@2.16.0:', type=('build', 'run'))
    depends_on('r-edger', when='@2.16.0:', type=('build', 'run'))
    depends_on('r-ggbio', when='@2.16.0:', type=('build', 'run'))
    depends_on('r-ggplot2', when='@2.16.0:', type=('build', 'run'))
    depends_on('r-gostats', when='@2.16.0:', type=('build', 'run'))
    depends_on('r-gseabase', when='@2.16.0:', type=('build', 'run'))
    depends_on('r-hwriter', when='@2.16.0:', type=('build', 'run'))
    depends_on('r-iranges', when='@2.16.0:', type=('build', 'run'))
    depends_on('r-knitr', when='@2.16.0:', type=('build', 'run'))
    depends_on('r-lattice', when='@2.16.0:', type=('build', 'run'))
    depends_on('r-limma(>=@3.17.5:', when='@2.16.0:', type=('build', 'run'))
    depends_on('r-pfam-db', when='@2.16.0:', type=('build', 'run'))
    depends_on('r-utils', when='@2.16.0:', type=('build', 'run'))
    depends_on('r-xml', when='@2.16.0:', type=('build', 'run'))

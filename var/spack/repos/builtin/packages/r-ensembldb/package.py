# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class REnsembldb(RPackage):
    """The package provides functions to create and use transcript centric
       annotation databases/packages. The annotation for the databases are
       directly fetched from Ensembl using their Perl API. The functionality
       and data is similar to that of the TxDb packages from the
       GenomicFeatures package, but, in addition to retrieve all
       gene/transcript models and annotations from the database, the ensembldb
       package provides also a filter framework allowing to retrieve
       annotations for specific entries like genes encoded on a chromosome
       region or transcript models of lincRNA genes."""

    homepage = "https://bioconductor.org/packages/ensembldb/"
    git      = "https://git.bioconductor.org/packages/ensembldb.git"

    version('2.0.4', commit='514623d71e3cca7a4e547adb579b5a958702ef86')

    depends_on('r-biocgenerics', type=('build', 'run'))
    depends_on('r-genomicranges', type=('build', 'run'))
    depends_on('r-genomicfeatures', type=('build', 'run'))
    depends_on('r-annotationfilter', type=('build', 'run'))
    depends_on('r-rsqlite', type=('build', 'run'))
    depends_on('r-dbi', type=('build', 'run'))
    depends_on('r-biobase', type=('build', 'run'))
    depends_on('r-genomeinfodb', type=('build', 'run'))
    depends_on('r-annotationdbi', type=('build', 'run'))
    depends_on('r-rtracklayer', type=('build', 'run'))
    depends_on('r-s4vectors', type=('build', 'run'))
    depends_on('r-annotationhub', type=('build', 'run'))
    depends_on('r-rsamtools', type=('build', 'run'))
    depends_on('r-iranges', type=('build', 'run'))
    depends_on('r-protgenerics', type=('build', 'run'))
    depends_on('r-biostrings', type=('build', 'run'))
    depends_on('r-curl', type=('build', 'run'))
    depends_on('r@3.4.0:3.4.9', type=('build', 'run'))

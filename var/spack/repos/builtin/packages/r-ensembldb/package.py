# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class REnsembldb(RPackage):
    """Utilities to create and use Ensembl-based annotation databases

       The package provides functions to create and use transcript centric
       annotation databases/packages. The annotation for the databases are
       directly fetched from Ensembl using their Perl API. The functionality
       and data is similar to that of the TxDb packages from the
       GenomicFeatures package, but, in addition to retrieve all
       gene/transcript models and annotations from the database, ensembldb
       provides a filter framework allowing to retrieve annotations for
       specific entries like genes encoded on a chromosome region or transcript
       models of lincRNA genes. EnsDb databases built with ensembldb contain
       also protein annotations and mappings between proteins and their
       encoding transcripts. Finally, ensembldb provides functions to map
       between genomic, transcript and protein coordinates."""

    homepage = "https://bioconductor.org/packages/ensembldb"
    git      = "https://git.bioconductor.org/packages/ensembldb.git"

    version('2.8.0', commit='b35f4c97d6d1890d8a9dbc0d31a8b63b008c35ac')
    version('2.6.8', commit='c2c4f41b4ecc81d5328ce1d380065dfcb5e0c54c')
    version('2.4.1', commit='b5b6b94826a2f46a4faecb9dde750ecd3bfaf327')
    version('2.2.2', commit='d71610e58aed88dbbe6a74e7a8ddfb7451398060')
    version('2.0.4', commit='514623d71e3cca7a4e547adb579b5a958702ef86')

    depends_on('r@3.6.0:3.6.9', when='@2.8.0', type=('build', 'run'))
    depends_on('r@3.5.0:3.5.9', when='@2.6.8', type=('build', 'run'))
    depends_on('r@3.5.0:3.5.9', when='@2.4.1', type=('build', 'run'))
    depends_on('r@3.4.0:3.4.9', when='@2.2.2', type=('build', 'run'))
    depends_on('r@3.4.0:3.4.9', when='@2.0.4', type=('build', 'run'))

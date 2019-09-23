# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlBioperl(PerlPackage):
    """BioPerl is the product of a community effort to produce Perl code which
    is useful in biology. Examples include Sequence objects, Alignment objects
    and database searching objects. These objects not only do what they are
    advertised to do in the documentation, but they also interact - Alignment
    objects are made from the Sequence objects, Sequence objects have access to
    Annotation and SeqFeature objects and databases, Blast objects can be
    converted to Alignment objects, and so on. This means that the objects
    provide a coordinated and extensible framework to do computational biology.

    BioPerl development focuses on Perl classes, or code that is used to create
    objects representing biological entities. There are scripts provided in the
    scripts/ and examples/ directories but scripts are not the main focus of
    the BioPerl developers. Of course, as the objects do most of the hard work
    for you, all you have to do is combine a number of objects together
    sensibly to make useful scripts.

    The intent of the BioPerl development effort is to make reusable tools that
    aid people in creating their own sites or job-specific applications.

    The BioPerl website at http://bioperl.org also attempts to maintain links
    and archives of standalone bio-related Perl tools that are not affiliated
    or related to the core BioPerl effort. Check the site for useful code ideas
    and contribute your own if possible."""

    homepage = "https://metacpan.org/pod/BioPerl"
    url      = "https://cpan.metacpan.org/authors/id/C/CD/CDRAUG/BioPerl-1.7.6.tar.gz"

    version('1.7.6', sha256='df2a3efc991b9b5d7cc9d038a1452c6dac910c9ad2a0e47e408dd692c111688d')

    depends_on('perl-data-stag', type=('build', 'run'))
    depends_on('perl-error', type=('build', 'run'))
    depends_on('perl-graph', type=('build', 'run'))
    depends_on('perl-http-message', type=('build', 'run'))
    depends_on('perl-io-string', type=('build', 'run'))
    depends_on('perl-io-stringy', type=('build', 'run'))
    depends_on('perl-ipc-run', type=('build', 'run'))
    depends_on('perl-list-moreutils', type=('build', 'run'))
    depends_on('perl-module-build', type=('build', 'run'))
    depends_on('perl-set-scalar', type=('build', 'run'))
    depends_on('perl-test-most', type=('build', 'run'))
    depends_on('perl-test-requiresinternet', type=('build', 'run'))
    depends_on('perl-uri', type=('build', 'run'))
    depends_on('perl-xml-dom', type=('build', 'run'))
    depends_on('perl-xml-dom-xpath', type=('build', 'run'))
    depends_on('perl-xml-libxml', type=('build', 'run'))
    depends_on('perl-xml-sax', type=('build', 'run'))
    depends_on('perl-xml-sax-base', type=('build', 'run'))
    depends_on('perl-xml-sax-writer', type=('build', 'run'))
    depends_on('perl-xml-twig', type=('build', 'run'))
    depends_on('perl-xml-writer', type=('build', 'run'))
    depends_on('perl-yaml', type=('build', 'run'))
    depends_on('perl-libwww-perl', type=('build', 'run'))
    depends_on('perl-libxml-perl', type=('build', 'run'))

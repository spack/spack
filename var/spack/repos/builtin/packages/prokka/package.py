# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Prokka(Package):
    """Prokka is a software tool to annotate bacterial, archaeal and viral
    genomes quickly and produce standards-compliant output files."""

    homepage = "https://github.com/tseemann/prokka"
    url      = "https://github.com/tseemann/prokka/archive/v1.13.tar.gz"

    version('1.13.4', sha256='19a699effe3fd38b3b50007473634161a1749eb7af00d1a67c42afa20446e5e3')
    version('1.13', '168193a4c61263759784564581523640')
    version('1.12', '658c4c203ddded3623e68a36f94cabec')

    depends_on('aragorn', type='run')
    depends_on('blast-plus', type='run')
    depends_on('hmmer', type='run')
    depends_on('infernal', type='run')
    depends_on('minced', type='run')
    depends_on('parallel', type='run')
    depends_on('perl', type='run')
    depends_on('perl-bio-perl', type='run')
    depends_on('perl-html-parser', type='run')
    depends_on('perl-swissknife', type='run')
    depends_on('perl-text-unidecode', type='run')
    depends_on('perl-xml-simple', type='run')
    depends_on('prodigal', type='run')
    depends_on('signalp', type='run')

    def install(self, spec, prefix):
        install_tree('bin', prefix.bin)
        install_tree('db', prefix.db)

        # Use bundled tbl2asn binary until PR#6875 is merged
        install('binaries/linux/tbl2asn', prefix.bin)

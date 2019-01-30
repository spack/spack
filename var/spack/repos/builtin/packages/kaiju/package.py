# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Kaiju(MakefilePackage):
    """Kaiju is a program for the taxonomic classification
    of high-throughput sequencing reads."""

    homepage = "https://github.com/bioinformatics-centre/kaiju"
    url      = "https://github.com/bioinformatics-centre/kaiju/archive/v1.6.2.zip"

    version('1.6.2', '0bd85368954837aa31f3de8b87ea410b')

    build_directory = 'src'

    depends_on('perl-io-compress', type='run')
    depends_on('py-htseq', type='run')

    def edit(self, spec, prefix):
        # Replace ftp:// with https://
        makedb = FileFilter('util/makeDB.sh')
        makedb.filter('ftp://', 'https://', string=True)

    def install(self, spec, prefix):
        install_tree('bin', prefix.bin)

# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Bowtie(MakefilePackage):
    """Bowtie is an ultrafast, memory efficient short read aligner
    for short DNA sequences (reads) from next-gen sequencers."""

    homepage = "https://sourceforge.net/projects/bowtie-bio/"
    url      = "https://downloads.sourceforge.net/project/bowtie-bio/bowtie/1.2.1.1/bowtie-1.2.1.1-src.zip"

    version('1.2.1.1', 'ec06265730c5f587cd58bcfef6697ddf')

    variant("tbb", default=False, description="Use Intel thread building block")

    depends_on("tbb", when="+tbb")

    def edit(self, spec, prefix):
        makefile = FileFilter("Makefile")
        makefile.filter('CC= .*', 'CC = ' + env['CC'])
        makefile.filter('CXX = .*', 'CXX = ' + env['CXX'])

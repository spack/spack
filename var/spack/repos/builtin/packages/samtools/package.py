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


class Samtools(Package):
    """SAM Tools provide various utilities for manipulating alignments in
       the SAM format, including sorting, merging, indexing and generating
       alignments in a per-position format"""

    homepage = "www.htslib.org"
    url = "https://github.com/samtools/samtools/releases/download/1.3.1/samtools-1.3.1.tar.bz2"

    version('1.9', 'cca9a40d9b91b007af2ff905cb8b5924')
    version('1.8', 'c6e981c92ca00a44656a708c4b52aba3')
    version('1.7', '2240175242b5183bfa6baf1483f68023')
    version('1.6', 'b756f05fd5d1a7042074417edb8c9aea')
    version('1.4', '8cbd7d2a0ec16d834babcd6c6d85d691')
    version('1.3.1', 'a7471aa5a1eb7fc9cc4c6491d73c2d88')
    version('1.2', '988ec4c3058a6ceda36503eebecd4122')

    depends_on('ncurses')
    # htslib became standalone @1.3.1, must use corresponding version
    depends_on('htslib@1.9',   when='@1.9')
    depends_on('htslib@1.8',   when='@1.8')
    depends_on('htslib@1.7',   when='@1.7')
    depends_on('htslib@1.6',   when='@1.6')
    depends_on('htslib@1.4',   when='@1.4')
    depends_on('htslib@1.3.1', when='@1.3.1')
    depends_on('zlib', when='@1.7:')
    depends_on('bzip2', when='@1.7:')

    def install(self, spec, prefix):
        if self.spec.version >= Version('1.3.1'):
            configure('--prefix={0}'.format(prefix), '--with-ncurses',
                      'CURSES_LIB=-lncursesw')
            make()
            make('install')
        else:
            make("prefix=%s" % prefix)
            make("prefix=%s" % prefix, "install")
        # Install dev headers and libs for legacy apps depending on them
        mkdir(prefix.include)
        mkdir(prefix.lib)
        install('sam.h', prefix.include)
        install('bam.h', prefix.include)
        install('libbam.a', prefix.lib)

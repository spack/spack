##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
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


class TrnascanSe(MakefilePackage):
    """A program for improved detection of transfer RNA genes in genomic
       sequence."""

    homepage = "http://lowelab.ucsc.edu/tRNAscan-SE/"
    url      = "http://lowelab.ucsc.edu/software/tRNAscan-SE-1.3.1.tar.gz"

    version('1.3.1', '714689121a1cf11c5d9c59561769c4d7')

    depends_on('perl', type=('build', 'run'))

    # Had to get kind of hacky to get around the $(HOME) variable in the
    # paths below in the Makefile
    def edit(self, spec, prefix):
        makefile = FileFilter('Makefile')
        makefile.filter('PERLDIR = /usr/bin', 'PERLDIR = %s'
                        % self.spec['perl'].prefix.bin)
        makefile.filter('BINDIR  = ', 'BINDIR = %s \n#'
                        % prefix.bin)
        makefile.filter('LIBDIR  = ', 'LIBDIR = %s \n#'
                        % prefix.lib)
        makefile.filter('MANDIR  = ', 'MANDIR = %s \n#'
                        % prefix.share.man)
        
    def setup_environment(self, spack_env, run_env):
        run_env.prepend_path('PERL5LIB', prefix.bin)

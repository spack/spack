##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
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


class Shoremap(Package):
    """Whole genome resequencing of pools of recombinant mutant genomes allows
       directly linking phenotypic traits to causal mutations. Such an
       analysis, called mapping-by-sequencing, combines classical genetic
       mapping and next generation sequencing by relying on selection-induced
       patterns within genome-wide allele frequency in pooled genomes. SHOREmap
       is a computational tool implementing a method that enables simple and
       straightforward mapping-by-sequencing analysis."""

    homepage = "http://bioinfo.mpipz.mpg.de/shoremap/"
    url      = "http://bioinfo.mpipz.mpg.de/shoremap/SHOREmap_v3.6.tar.gz"

    version('3.6', 'ccc9331189705a139d50f2c161178cb1')

    depends_on('dislin')

    def patch(self):
        makefile = FileFilter('makefile')
        makefile.filter(r'-L/usr/lib/ ',
                        '-L' + self.spec['libxt'].prefix.lib + ' ')
        makefile.filter(r'-L\./dislin.* -ldislin',
                        '-L' + self.spec['dislin'].prefix + ' -ldislin')

    def setup_environment(self, spack_env, run_env):
        spack_env.prepend_path('LD_LIBRARY_PATH', self.spec['dislin'].prefix)
        run_env.prepend_path('LD_LIBRARY_PATH', self.spec['dislin'].prefix)
        run_env.prepend_path('PATH', join_path(self.prefix, 'bin'))

    def install(self, spec, prefix):
        make()
        mkdirp(prefix.bin)
        install('SHOREmap', prefix.bin)

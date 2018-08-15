##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the LICENSE file for our notice and the LGPL.
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


class Augustus(MakefilePackage):
    """AUGUSTUS is a program that predicts genes in eukaryotic
       genomic sequences"""

    homepage = "http://bioinf.uni-greifswald.de/augustus/"
    url      = "http://bioinf.uni-greifswald.de/augustus/binaries/augustus-3.3.1.tar.gz"
    list_url = "http://bioinf.uni-greifswald.de/augustus/binaries/old"

    version('3.3.1', '8363ece221c799eb169f47e545efb951')
    version('3.3',   '93691d9aafc7d3d0e1adf31ec308507f')
    version('3.2.3', 'b8c47ea8d0c45aa7bb9a82626c8ff830')

    depends_on('bamtools')
    depends_on('gsl')
    depends_on('boost')
    depends_on('zlib')

    def edit(self, spec, prefix):
        with working_dir(join_path('auxprogs', 'filterBam', 'src')):
            makefile = FileFilter('Makefile')
            makefile.filter('BAMTOOLS = .*', 'BAMTOOLS = %s' % self.spec[
                            'bamtools'].prefix)
            makefile.filter('INCLUDES = *',
                            'INCLUDES = -I$(BAMTOOLS)/include/bamtools ')
            if 'bamtools@2.5:' in spec:
                makefile.filter('LIBS = -lbamtools -lz',
                                'LIBS = $(BAMTOOLS)/lib64/'
                                '/libbamtools.a -lz')
            if 'bamtools@:2.4' in spec:
                makefile.filter('LIBS = -lbamtools -lz',
                                'LIBS = $(BAMTOOLS)/lib/bamtools'
                                '/libbamtools.a -lz')
        with working_dir(join_path('auxprogs', 'bam2hints')):
            makefile = FileFilter('Makefile')
            makefile.filter('# Variable definition',
                            'BAMTOOLS = %s' % self.spec['bamtools'].prefix)
            makefile.filter('INCLUDES = /usr/include/bamtools',
                            'INCLUDES = $(BAMTOOLS)/include/bamtools')
            if 'bamtools@2.5:' in spec:
                makefile.filter('LIBS = -lbamtools -lz',
                                'LIBS = $(BAMTOOLS)/lib64/'
                                '/libbamtools.a -lz')
            if 'bamtools@:2.4' in spec:
                makefile.filter('LIBS = -lbamtools -lz',
                                'LIBS = $(BAMTOOLS)/lib/bamtools'
                                '/libbamtools.a -lz')

    def install(self, spec, prefix):
        install_tree('bin', join_path(self.spec.prefix, 'bin'))
        install_tree('config', join_path(self.spec.prefix, 'config'))
        install_tree('scripts', join_path(self.spec.prefix, 'scripts'))

    def setup_environment(self, spack_env, run_env):
        run_env.set('AUGUSTUS_CONFIG_PATH', join_path(
            self.prefix, 'config'))
        run_env.prepend_path('PATH', join_path(self.prefix, 'scripts'))

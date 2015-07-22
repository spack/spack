##############################################################################
# Copyright (c) 2015, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Written by Mark C. Miller, miller86@llnl.gov All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://scalability-llnl.github.io/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License (as published by
# the Free Software Foundation) version 2.1 dated February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *
import glob

class SuperluDist(Package):
    """SuperLU is a general purpose library for the direct solution of large,
       sparse, nonsymmetric systems of linear equations on high performance machines.
       There are three variants of SuperLU; The sequential version (SuperLU), a
       multi-threaded parallel version (SuperLU-MT) and a distributed memory
       parallel version, (SuperLU-DIST). This is the DIST version.
    """

    homepage = "http://crd-legacy.lbl.gov/~xiaoye/SuperLU/"
    url      = "http://crd-legacy.lbl.gov/~xiaoye/SuperLU/superlu_dist_4.1.tar.gz"
    list_url = "http://crd-legacy.lbl.gov/~xiaoye/SuperLU/"
    list_depth = 0

    version('4.1', 'ec70d4d1d07aa058c09feb1d3413c738')

    # global variants
    variant('debug', default=False, description="Enable debugging")
    variant('static', default=False, description="Build only static libs.")

    # package specific variants
    variant('fortran', default=True, description="Enable Fortran interfaces.")

#    depends_on('mpi')
    depends_on('metis')
    depends_on('parmetis')

    def install(self, spec, prefix):

        files = ['make.inc']

        filter_file('^BLASDEF','#BLASDEF', *files)
        filter_file('^METISLIB := (.*)','METISLIB := -L%s/lib -lmetis' % spec['metis'].prefix, *files)
        filter_file('^PARMETISLIB := (.*)','PARMETISLIB := -L%s/lib -lparmetis' % spec['parmetis'].prefix, *files)
        filter_file('^I_PARMETIS := (.*)','I_PARMETIS := %s/include' % spec['parmetis'].prefix, *files)

        if spec.satisfies('@4.1'):
            filter_file('^DSuperLUroot(.*)','DSuperLUroot = %s' % spec['superlu-dist'].prefix, *files)
            filter_file('^DSUPERLULIB(.*)','DSUPERLULIB = %s/lib/libsuperlu_dist.a' % spec['superlu-dist'].prefix, *files)

        if '+debug' in spec:
            filter_file('^CFLAGS( *)=(.*)','CFLAGS = $(I_PARMETIS) -g -std=c99 -Wall -DDEBUGlevel=3 -DPRNTlevel=3 -DPROFlevel=3', *files)
        else:
            filter_file('^CFLAGS( *)=(.*)','CFLAGS = $(I_PARMETIS) -std=c99 -DDEBUGlevel=0 -DPRNTlevel=0 -DPROFlevel=0', *files)

#
#        if '+static' in spec:
#            config_args += ["--disable-shared", "--enable-static"]
#        else:
#            config_args += ["--enable-shared", "--enable-static"]
#
#        # Enable fortran interface if we have a fortran compiler and
#        # fortran API isn't explicitly disabled
#        if self.compiler.fc and '~fortran' not in spec:
#            config_args += ["--enable-fortran", "--enable-fortran2003"]

        mkdirp(prefix.lib)
        mkdirp(prefix.include)

        make("lib", parallel=False)
        #install('SRC/libsuperlu_dist.a', prefix.lib)
        for f in glob.glob('SRC/*.h'):
            install(f, prefix.include)

    def url_for_version(self, version):
        v = str(version)

        return "http://crd-legacy.lbl.gov/~xiaoye/SuperLU/superlu_dist_" + v + ".tar.gz"

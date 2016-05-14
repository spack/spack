##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
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
import glob

class SuperluDist(Package):
    """A general purpose library for the direct solution of large, sparse, nonsymmetric systems of linear equations on high performance machines."""
    homepage = "http://crd-legacy.lbl.gov/~xiaoye/SuperLU/"
    url      = "http://crd-legacy.lbl.gov/~xiaoye/SuperLU/superlu_dist_4.1.tar.gz"

    version('5.0.0', '2b53baf1b0ddbd9fcf724992577f0670')
    # default to version 4.3 since petsc and trilinos are not tested with 5.0.
    version('4.3', 'ee66c84e37b4f7cc557771ccc3dc43ae', preferred=True)
    version('4.2', 'ae9fafae161f775fbac6eba11e530a65')
    version('4.1', '4edee38cc29f687bd0c8eb361096a455')
    version('4.0', 'c0b98b611df227ae050bc1635c6940e0')

    depends_on ('mpi')
    depends_on ('blas')
    depends_on ('lapack')
    depends_on ('parmetis')
    depends_on ('metis@5:')

    def install(self, spec, prefix):
        makefile_inc = []
        makefile_inc.extend([
            'PLAT         = _mac_x',
            'DSuperLUroot = %s' % self.stage.source_path, #self.stage.path, prefix
            'DSUPERLULIB  = $(DSuperLUroot)/lib/libsuperlu_dist.a',
            'BLASDEF      = -DUSE_VENDOR_BLAS',
            'BLASLIB      = -L%s -llapack %s -lblas' % (spec['lapack'].prefix.lib, spec['blas'].prefix.lib), # FIXME: avoid hardcoding blas/lapack lib names
            'METISLIB     = -L%s -lmetis' % spec['metis'].prefix.lib,
            'PARMETISLIB  = -L%s -lparmetis' % spec['parmetis'].prefix.lib,
            'FLIBS        =',
            'LIBS         = $(DSUPERLULIB) $(BLASLIB) $(PARMETISLIB) $(METISLIB)',
            'ARCH         = ar',
            'ARCHFLAGS    = cr',
            'RANLIB       = true',
            'CC           = mpicc', # FIXME avoid hardcoding MPI compiler names
            'CFLAGS       = -fPIC -std=c99 -O2 -I%s -I%s' %(spec['parmetis'].prefix.include, spec['metis'].prefix.include),
            'NOOPTS       = -fPIC -std=c99',
            'FORTRAN      = mpif77',
            'F90FLAGS     = -O2',
            'LOADER       = mpif77',
            'LOADOPTS     =',
            'CDEFS        = -DAdd_'
            ])

        #with working_dir('src'):
        with open('make.inc', 'w') as fh:
            fh.write('\n'.join(makefile_inc))

        make("lib", parallel=False)

        # FIXME:
        # cd "EXAMPLE" do
        # system "make"

        # need to install by hand
        headers_location = self.prefix.include
        mkdirp(headers_location)
        mkdirp(prefix.lib)

        headers = glob.glob(join_path(self.stage.source_path, 'SRC','*.h'))
        for h in headers:
            install(h,headers_location)

        superludist_lib = join_path(self.stage.source_path, 'lib/libsuperlu_dist.a')
        install(superludist_lib,self.prefix.lib)

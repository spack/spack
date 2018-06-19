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


class Elpa(AutotoolsPackage):
    """Eigenvalue solvers for Petaflop-Applications (ELPA)"""

    homepage = 'http://elpa.mpcdf.mpg.de/'
    url = 'http://elpa.mpcdf.mpg.de/elpa-2015.11.001.tar.gz'

    version('2018.05.001.rc1', 'ccd77bd8036988ee624f43c04992bcdd')
    version('2017.11.001', '4a437be40cc966efb07aaab84c20cd6e', preferred=True)
    version('2017.05.003', '7c8e5e58cafab212badaf4216695700f')
    version('2017.05.002', 'd0abc1ac1f493f93bf5e30ec8ab155dc')
    version('2016.11.001.pre', '5656fd066cf0dcd071dbcaf20a639b37')
    version('2016.05.004', 'c0dd3a53055536fc3a2a221e78d8b376')
    version('2016.05.003', '88a9f3f3bfb63e16509dd1be089dcf2c')
    version('2015.11.001', 'de0f35b7ee7c971fd0dca35c900b87e6')

    variant('openmp', default=False, description='Activates OpenMP support')
    variant('optflags', default=True, description='Build with optimization flags')

    depends_on('mpi')
    depends_on('blas')
    depends_on('lapack')
    depends_on('scalapack')

    def url_for_version(self, version):
        t = 'http://elpa.mpcdf.mpg.de/html/Releases/{0}/elpa-{0}.tar.gz'
        if version < Version('2016.05.003'):
            t = 'http://elpa.mpcdf.mpg.de/elpa-{0}.tar.gz'
        return t.format(str(version))

    # override default implementation which returns static lib
    @property
    def libs(self):
        libname = 'libelpa_openmp' if '+openmp' in self.spec else 'libelpa'
        return find_libraries(
            libname, root=self.prefix, shared=True, recursive=True
        )

    build_directory = 'spack-build'

    def setup_environment(self, spack_env, run_env):
        spec = self.spec

        spack_env.set('CC', spec['mpi'].mpicc)
        spack_env.set('FC', spec['mpi'].mpifc)
        spack_env.set('CXX', spec['mpi'].mpicxx)

        spack_env.append_flags('LDFLAGS', spec['lapack'].libs.search_flags)
        spack_env.append_flags('LIBS', spec['lapack'].libs.link_flags)
        spack_env.set('SCALAPACK_LDFLAGS', spec['scalapack'].libs.joined())

    def configure_args(self):
        # TODO: set optimum flags for platform+compiler combo, see
        # https://github.com/hfp/xconfigure/tree/master/elpa
        # also see:
        # https://src.fedoraproject.org/cgit/rpms/elpa.git/
        # https://packages.qa.debian.org/e/elpa.html
        options = []
        # without -march=native there is configure error for 2017.05.02
        # Could not compile test program, try with --disable-sse, or
        # adjust the C compiler or CFLAGS
        if '+optflags' in self.spec:
            options.extend([
                'FCFLAGS=-O2 -march=native -ffree-line-length-none',
                'CFLAGS=-O2 -march=native'
            ])
        if '+openmp' in self.spec:
            options.append('--enable-openmp')
        return options

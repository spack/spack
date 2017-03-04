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
from spack.package_test import *
from spack.util.executable import Executable
import os.path


class Atlas(Package):
    """Automatically Tuned Linear Algebra Software, generic shared ATLAS is an
    approach for the automatic generation and optimization of numerical
    software. Currently ATLAS supplies optimized versions for the complete set
    of linear algebra kernels known as the Basic Linear Algebra Subroutines
    (BLAS), and a subset of the linear algebra routines in the LAPACK library.
    """
    homepage = "http://math-atlas.sourceforge.net/"

    version('3.10.3', 'd6ce4f16c2ad301837cfb3dade2f7cef',
            url='https://sourceforge.net/projects/math-atlas/files/Stable/3.10.3/atlas3.10.3.tar.bz2')

    version('3.10.2', 'a4e21f343dec8f22e7415e339f09f6da',
            url='https://sourceforge.net/projects/math-atlas/files/Stable/3.10.2/atlas3.10.2.tar.bz2', preferred=True)
    # not all packages (e.g. Trilinos@12.6.3) stopped using deprecated in 3.6.0
    # Lapack routines. Stick with 3.5.0 until this is fixed.
    resource(name='lapack',
             url='http://www.netlib.org/lapack/lapack-3.5.0.tgz',
             md5='b1d3e3e425b2e44a06760ff173104bdf',
             destination='spack-resource-lapack',
             when='@3:')

    version('3.11.34', '0b6c5389c095c4c8785fd0f724ec6825',
            url='http://sourceforge.net/projects/math-atlas/files/Developer%20%28unstable%29/3.11.34/atlas3.11.34.tar.bz2')

    variant('shared', default=True, description='Builds shared library')
    variant('pthread', default=False, description='Use multithreaded libraries')

    provides('blas')
    provides('lapack')

    parallel = False

    def patch(self):
        # Disable thread check.  LLNL's environment does not allow
        # disabling of CPU throttling in a way that ATLAS actually
        # understands.
        filter_file(r'^\s+if \(thrchk\) exit\(1\);', 'if (0) exit(1);',
                    'CONFIG/src/config.c')
        # TODO: investigate a better way to add the check back in
        # TODO: using, say, MSRs.  Or move this to a variant.

    def install(self, spec, prefix):
        # reference to other package managers
        # https://github.com/hpcugent/easybuild-easyblocks/blob/master/easybuild/easyblocks/a/atlas.py
        # https://github.com/macports/macports-ports/blob/master/math/atlas/Portfile
        # https://github.com/Homebrew/homebrew-science/pull/3571
        options = []
        if '+shared' in spec:
            options.extend([
                '--shared'
            ])
            # TODO: for non GNU add '-Fa', 'alg', '-fPIC' ?

        # configure for 64-bit build
        options.extend([
            '-b', '64'
        ])

        # set compilers:
        options.extend([
            '-C', 'ic', spack_cc,
            '-C', 'if', spack_f77
        ])

        # Lapack resource to provide full lapack build. Note that
        # ATLAS only provides a few LAPACK routines natively.
        options.append('--with-netlib-lapack-tarfile=%s' %
                       self.stage[1].archive_file)

        with working_dir('spack-build', create=True):
            configure = Executable('../configure')
            configure('--prefix=%s' % prefix, *options)
            make()
            make('check')
            make('ptcheck')
            make('time')
            if '+shared' in spec:
                with working_dir('lib'):
                    make('shared_all')

            make("install")
            self.install_test()

    @property
    def libs(self):
        # libsatlas.[so,dylib,dll ] contains all serial APIs (serial lapack,
        # serial BLAS), and all ATLAS symbols needed to support them. Whereas
        # libtatlas.[so,dylib,dll ] is parallel (multithreaded) version.
        is_threaded = '+pthread' in self.spec
        if '+shared' in self.spec:
            to_find = ['libtatlas'] if is_threaded else ['libsatlas']
            shared = True
        else:
            interfaces = [
                'libptcblas',
                'libptf77blas'
            ] if is_threaded else [
                'libcblas',
                'libf77blas'
            ]
            to_find = ['liblapack'] + interfaces + ['libatlas']
            shared = False
        return find_libraries(
            to_find, root=self.prefix, shared=shared, recurse=True
        )

    def install_test(self):
        source_file = join_path(os.path.dirname(self.module.__file__),
                                'test_cblas_dgemm.c')
        blessed_file = join_path(os.path.dirname(self.module.__file__),
                                 'test_cblas_dgemm.output')

        include_flags = ["-I%s" % self.spec.prefix.include]
        link_flags = self.libs.ld_flags.split()

        output = compile_c_and_execute(source_file, include_flags, link_flags)
        compare_output_file(output, blessed_file)

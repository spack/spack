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


class M4(AutotoolsPackage):
    """GNU M4 is an implementation of the traditional Unix macro processor."""

    homepage = "https://www.gnu.org/software/m4/m4.html"
    url      = "https://ftpmirror.gnu.org/m4/m4-1.4.18.tar.gz"

    version('1.4.18', 'a077779db287adf4e12a035029002d28')
    version('1.4.17', 'a5e9954b1dae036762f7b13673a2cf76')

    patch('gnulib-pgi.patch', when='@1.4.18')
    patch('pgi.patch', when='@1.4.17')
    # from: https://github.com/Homebrew/homebrew-core/blob/master/Formula/m4.rb
    # Patch credit to Jeremy Huddleston Sequoia <jeremyhu@apple.com>
    patch('secure_snprintf.patch', when='platform_os = highsierra')

    variant('sigsegv', default=True,
            description="Build the libsigsegv dependency")

    depends_on('libsigsegv', when='+sigsegv')

    build_directory = 'spack-build'

    def configure_args(self):
        spec = self.spec
        args = ['--enable-c++']

        if spec.satisfies('%clang') and not spec.satisfies('platform=darwin'):
            args.append('CFLAGS=-rtlib=compiler-rt')

        if spec.satisfies('%intel'):
            args.append('CFLAGS=-no-gcc')

        if '+sigsegv' in spec:
            args.append('--with-libsigsegv-prefix={0}'.format(
                spec['libsigsegv'].prefix))
        else:
            args.append('--without-libsigsegv-prefix')

        # http://lists.gnu.org/archive/html/bug-m4/2016-09/msg00002.html
        arch = spec.architecture
        if (arch.platform == 'darwin' and arch.platform_os == 'sierra' and
            '%gcc' in spec):
            args.append('ac_cv_type_struct_sched_param=yes')

        return args

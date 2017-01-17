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


class Libxsmm(Package):
    '''LIBXSMM is a library for small dense and small sparse matrix-matrix
    multiplications targeting Intel Architecture (x86).'''

    homepage = 'https://github.com/hfp/libxsmm'
    url      = 'https://github.com/hfp/libxsmm/archive/1.4.3.tar.gz'

    version('1.4.3', '9839bf0fb8be7badf1e97ce4c817149b')
    version('1.4.2', 'ea025761437f3b5c936821b9ca21ec31')
    version('1.4.1', '71648500ea4510529845d329091917df')
    version('1.4',   'b42f91bf5285e7ad0463446e55ebdc2b')

    def patch(self):
        kwargs = {'ignore_absent': False, 'backup': False, 'string': True}
        makefile = FileFilter('Makefile.inc')

        # Spack sets CC, CXX, and FC to point to the compiler wrappers
        # Don't let Makefile.inc overwrite these
        makefile.filter('CC = icc',         'CC ?= icc', **kwargs)
        makefile.filter('CC = gcc',         'CC ?= gcc', **kwargs)
        makefile.filter('CXX = icpc',       'CXX ?= icpc', **kwargs)
        makefile.filter('CXX = g++',        'CXX ?= g++', **kwargs)
        makefile.filter('FC = ifort',       'FC ?= ifort', **kwargs)
        makefile.filter('FC = gfortran',    'FC ?= gfortran', **kwargs)

    def manual_install(self, prefix):
        install_tree('include', prefix.include)
        install_tree('lib', prefix.lib)
        install_tree('documentation', prefix.share + '/libxsmm/doc')

    def install(self, spec, prefix):
        make_args = [
            'ROW_MAJOR=0',
            'INDICES_M={0}'.format(' '.join(str(i) for i in range(1, 25))),
            'INDICES_N={0}'.format(' '.join(str(i) for i in range(1, 25))),
            'INDICES_K={0}'.format(' '.join(str(i) for i in range(1, 25)))
        ]
        make(*make_args)
        self.manual_install(prefix)

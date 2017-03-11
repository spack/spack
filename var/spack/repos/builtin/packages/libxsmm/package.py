##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
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
from glob import glob


class Libxsmm(Package):
    '''Library targeting Intel Architecture
    for small, dense or sparse matrix multiplications,
    and small convolutions.'''

    homepage = 'https://github.com/hfp/libxsmm'
    url      = 'https://github.com/hfp/libxsmm/archive/1.7.1.tar.gz'

    version('develop', git='https://github.com/hfp/libxsmm.git')

    version('1.7.1', 'a938335b1c2c90616dc72c2c1a5824ab')
    version('1.7',   'cb3aff6d123ba70bd3d4daf575767d14')
    version('1.6.6', '8b45ae022f36b8c212f579a0952b5034')
    version('1.6.5', 'fa21fe88d092477fa796a346ac7674ff')
    version('1.6.4', '23e484f7b9f980c2a3819db6e6c68710')
    version('1.6.3', '7969c56e6faed66f9e07d86f063ecf0b')
    version('1.6.2', '1920e58fdf00d2635d24cf5c07007bfc')
    version('1.6.1', 'e3493c77c57d42cfa58e0e55a69ee22c')
    version('1.6',   '31c130aa176db23944de420b59e1c74d')
    version('1.5.2', 'ecda62ec3e5c60897d0d7780c524bc19')
    version('1.5.1', '612244e92024e11ec672bafb6e85c01b')
    version('1.5',   '7b550702b55dc8e73a42a2986a1e1b36')
    version('1.4.4', '78beefa57da02126cf4556f0eef3f8f0')
    version('1.4.3', '9839bf0fb8be7badf1e97ce4c817149b')
    version('1.4.2', 'ea025761437f3b5c936821b9ca21ec31')
    version('1.4.1', '71648500ea4510529845d329091917df')
    version('1.4',   'b42f91bf5285e7ad0463446e55ebdc2b')

    variant('debug', default=False,
            description='Unoptimized with call-trace (LIBXSMM_TRACE).')
    variant('header-only', default=False,
            description='Produce header-only installation')

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
        spec = self.spec
        install_tree('include', prefix.include)
        if '~header-only' in spec:
            install_tree('lib', prefix.lib)
        doc_path = prefix.share + '/libxsmm/doc'
        mkdirp(doc_path)
        for doc_file in glob('documentation/*.md'):
            install(doc_file, doc_path)
        for doc_file in glob('documentation/*.pdf'):
            install(doc_file, doc_path)
        install('README.md', doc_path)
        install('LICENSE', doc_path)

    def install(self, spec, prefix):
        if '+header-only' in spec and '@1.6.2:' not in spec:
            raise InstallError(
                "The variant +header-only is only available " +
                "for versions @1.6.2:")

        # include symbols by default
        make_args = ['SYM=1']

        if '+header-only' in spec:
            make_args += ['header-only']

        # JIT (AVX and later) makes MNK, M, N, or K spec. superfluous
#       make_args += ['MNK=1 4 5 6 8 9 13 16 17 22 23 24 26 32']

        # include call trace as the build is already de-optimized
        if '+debug' in spec:
            make_args += ['DBG=1']
            make_args += ['TRACE=1']

        make(*make_args)
        self.manual_install(prefix)

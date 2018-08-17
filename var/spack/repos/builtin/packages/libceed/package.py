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


class Libceed(Package):
    """The CEED API Library: Code for Efficient Extensible Discretizations."""

    homepage = "https://github.com/CEED/libCEED"
    git      = "https://github.com/CEED/libCEED.git"

    version('develop', branch='master')
    version('0.2', tag='v0.2')
    version('0.1', tag='v0.1')

    variant('occa', default=True, description='Enable OCCA backends')
    variant('cuda', default=False, description='Enable CUDA support')
    variant('debug', default=False, description='Enable debug build')

    depends_on('occa@v1.0.0-alpha.5,develop', when='+occa')
    depends_on('occa@develop', when='@develop+occa')
    depends_on('occa+cuda', when='+occa+cuda')
    depends_on('occa~cuda', when='+occa~cuda')

    # occa: do not occaFree kernels
    # Repeated creation and freeing of kernels appears to expose a caching
    # bug in Occa.
    patch('occaFree-0.2.diff', when='@0.2')

    phases = ['build', 'install']

    def build(self, spec, prefix):
        # Note: The occa package exports OCCA_DIR in the environment

        makeopts = ['V=1']
        makeopts += ['NDEBUG=%s' % ('' if '+debug' in spec else '1')]
        make(*makeopts)

        if self.run_tests:
            make('prove', *makeopts, parallel=False)

    def install(self, spec, prefix):
        make('install', 'prefix=%s' % prefix, parallel=False)

    @when('@0.1')
    def install(self, spec, prefix):
        mkdirp(prefix.include)
        install('ceed.h', prefix.include)
        mkdirp(prefix.lib)
        install('libceed.%s' % dso_suffix, prefix.lib)
        filter_file('^prefix=.*$', 'prefix=%s' % prefix, 'ceed.pc')
        filter_file('^includedir=\$\{prefix\}$',
                    'includedir=${prefix}/include', 'ceed.pc')
        filter_file('^libdir=\$\{prefix\}$', 'libdir=${prefix}/lib', 'ceed.pc')
        filter_file('Version:.*$', 'Version: 0.1', 'ceed.pc')
        mkdirp(prefix.lib.pkgconfig)
        install('ceed.pc', prefix.lib.pkgconfig)

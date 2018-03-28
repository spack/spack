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
    """The CEED API Library: Code for Efficient Extensible Discretizations
    """

    homepage = "https://github.com/CEED/libCEED"

    version('develop', git='https://github.com/CEED/libCEED.git',
            branch='master')
    # FIXME: replace all hash versions with '0.2' when it is tagged.
    version('a820fbc', git='https://github.com/CEED/libCEED.git',
            commit='a820fbcde076af5c5b50ef8dec742695f7fceea9')
    version('0.1', git='https://github.com/CEED/libCEED.git', tag='v0.1')

    variant('occa', default=True, description='Enable OCCA backends')
    variant('cuda', default=False, description='Enable CUDA support')
    variant('debug', default=False, description='Enable debug build')

    # FIXME: replace the occa hash-version with a tagged version?
    depends_on('occa@2db622c,develop', when='+occa')
    depends_on('occa@develop', when='@develop+occa')
    depends_on('occa+cuda', when='+occa+cuda')
    depends_on('occa~cuda', when='+occa~cuda')

    phases = ['build', 'install']

    def build(self, spec, prefix):
        # Note: The occa package exports OCCA_DIR in the environment

        # Note: FC is overwritten in the Makefile, so we need to force set the
        # value on the command line.
        makeopts = ['FC=%s' % env['FC'], 'V=1']
        if '~debug' in spec:
            makeopts += ['NDEBUG=1']
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

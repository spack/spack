##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
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
import glob


class IntelXed(Package):
    """The Intel X86 Encoder Decoder library for encoding and decoding x86
    machine instructions (64- and 32-bit).  Also includes libxed-ild,
    a lightweight library for decoding the length of an instruction."""

    homepage = "https://intelxed.github.io/"
    url = "https://github.com/intelxed/xed"

    version('2018.01.12',
            git = 'https://github.com/intelxed/xed',
            commit = '5c538047876feecf080d9441110f81d0e67b5de8')

    resource(name = 'mbuild',
             git = 'https://github.com/intelxed/mbuild',
             commit = 'bb9123152a330c7fa1ff1a502950dc199c83e177',
             destination = '')

    variant('debug', default=False, description='enable debug symbols')

    depends_on('python@2.7.0:', type='build')

    mycflags = []

    # Save CFLAGS for use in install.
    def flag_handler(self, name, flags):
        if name == 'cflags': self.mycflags = flags
        return (flags, None, None)

    def install(self, spec, prefix):
        mfile = Executable('./mfile.py')

        # Translate CFLAGS '-O2' to mbuild syntax.
        if '-O0' in self.mycflags: opt = '0'
        elif '-O' in self.mycflags: opt = '1'
        elif '-O1' in self.mycflags: opt = '1'
        elif '-O2' in self.mycflags: opt = '2'
        elif '-O3' in self.mycflags: opt = '3'
        else: opt = '2'

        args = ['-j', str(make_jobs),
                '--cc=%s' % spack_cc,
                '--opt=%s' % opt,
                '--no-werror']

        if '+debug' in spec: args.append('--debug')

        # Build and install static libxed.a.
        mfile('--clean')
        mfile(*args)

        mkdirp(prefix.include)
        mkdirp(prefix.lib)

        libs = glob.glob(join_path('obj', 'lib*.a'))
        for lib in libs:
            install(lib, prefix.lib)

        # Build and install shared libxed.so.
        mfile('--clean')
        mfile('--shared', *args)

        libs = glob.glob(join_path('obj', 'lib*.so'))
        for lib in libs:
            install(lib, prefix.lib)

        # Install header files.
        hdrs = glob.glob(join_path('include', 'public', 'xed', '*.h'))  \
            + glob.glob(join_path('obj', '*.h'))
        for hdr in hdrs:
            install(hdr, prefix.include)

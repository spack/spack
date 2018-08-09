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
import glob
import os


class IntelXed(Package):
    """The Intel X86 Encoder Decoder library for encoding and decoding x86
    machine instructions (64- and 32-bit).  Also includes libxed-ild,
    a lightweight library for decoding the length of an instruction."""

    homepage = "https://intelxed.github.io/"
    git      = "https://github.com/intelxed/xed.git"

    version('2018.02.14', commit='44d06033b69aef2c20ab01bfb518c52cd71bb537')

    resource(name='mbuild',
             git='https://github.com/intelxed/mbuild.git',
             commit='bb9123152a330c7fa1ff1a502950dc199c83e177',
             destination='')

    variant('debug', default=False, description='enable debug symbols')

    depends_on('python@2.7:', type='build')

    mycflags = []

    # Save CFLAGS for use in install.
    def flag_handler(self, name, flags):
        if name == 'cflags':
            self.mycflags = flags
        return (flags, None, None)

    def install(self, spec, prefix):
        # XED needs PYTHONPATH to find the mbuild directory.
        mbuild_dir = join_path(self.stage.source_path, 'mbuild')
        python_path = os.getenv('PYTHONPATH', '')
        os.environ['PYTHONPATH'] = mbuild_dir + ':' + python_path

        mfile = Executable('./mfile.py')

        args = ['-j', str(make_jobs),
                '--cc=%s' % spack_cc,
                '--no-werror']

        if '+debug' in spec:
            args.append('--debug')

        # If an optimization flag (-O...) is specified in CFLAGS, use
        # that, else set default opt level.
        for flag in self.mycflags:
            if len(flag) >= 2 and flag[0:2] == '-O':
                break
        else:
            args.append('--opt=2')

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

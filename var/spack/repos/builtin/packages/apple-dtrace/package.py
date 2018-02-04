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
import os.path


class AppleDtrace(Package):
    """apple-dtrace: tools from Apple's version of dtrace tracing framework

    Downloads Apple's version of the dtrace dynamic tracing framework
    and installs related tools. Does not install dtrace because it
    requires darwin kernel source headers.

    Installs:

    * libelf
    * libdwarf
    * libctf
    * ctfconvert
    * ctfdump
    * ctfmerge
    * additional headers used by memory instrumenting tool frameworks

    """

    homepage = "https://opensource.apple.com/tarballs/dtrace"
    url      = "https://opensource.apple.com/tarballs/dtrace/dtrace-209.50.12.tar.gz"

    version('209.50.12', 'e7f58979a1c47633593da2c8b7239ae6')

    # This project is only distributed as an Xcode project and has to be
    # built with Xcode.
    conflicts('%gcc')
    conflicts('%cce')

    provides('elf@0')  # FIXME: Not sure of version?
    # FIXME: also provides libdwarf; should this be virtual package?

    def install(self, spec, prefix):
        xcodebuild = which('xcodebuild')
        if xcodebuild is None:
            InstallError('xcodebuild must be installed to install dtrace!')

        xcodebuild('SYMROOT=build',
                   'DSTROOT={0}'.format(self.spec.prefix),
                   'SDKROOT={0}'.format(join_path('/Applications',
                                                  'Xcode.app',
                                                  'Contents',
                                                  'Developer',
                                                  'Platforms',
                                                  'MacOSX.platform',
                                                  'Developer',
                                                  'SDKs',
                                                  'MacOSX.sdk')),
                   '-target', 'libelf.a',
                   '-target', 'libdwarf.a',
                   '-target', 'libctf.a',
                   '-target', 'ctfconvert',
                   '-target', 'ctfdump',
                   '-target', 'ctfmerge')

        build_release = join_path('build', 'release')

        # Install executables
        mkdirp(prefix.bin)
        for f in glob.glob(join_path(build_release, 'ctf*')):
            install(f, join_path(prefix.bin, os.path.basename(f)))

        # Install libraries
        mkdirp(prefix.lib)
        for f in glob.glob(join_path('build', 'Release', '*.a')):
            install(f, join_path(prefix.lib, os.path.basename(f)))

        # Install headers
        mkdirp(prefix.include)
        install_tree('sys', prefix.include.sys)

        for f in glob.glob(join_path('head', '*.h')):
            install(f, join_path(prefix.include,
                                 os.path.basename(f)))

        for f in ['dwarf.h', 'libdwarf.h']:
            install(join_path('libdwarf', f),
                    join_path(prefix.include, f))

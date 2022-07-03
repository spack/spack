# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re

from spack.package import *


class Cpio(AutotoolsPackage, GNUMirrorPackage):
    """GNU cpio copies files into or out of a cpio or tar archive and the file system.
       The archive can be another file on the disk, a magnetic tape, or a pipe.
    """
    homepage = "https://www.gnu.org/software/cpio/"
    gnu_mirror_path = "cpio/cpio-2.13.tar.gz"

    executables = ['^cpio$']

    version('2.13', sha256='e87470d9c984317f658567c03bfefb6b0c829ff17dbf6b0de48d71a4c8f3db88')

    build_directory = 'spack-build'

    # See configure_args()
    conflicts('%intel@19')

    def patch(self):
        """Fix mutiple definition of char *program_name for gcc@10: and clang"""
        filter_file(r'char \*program_name;', '', 'src/global.c')

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)('--version', output=str, error=str)
        match = re.search(r'\(GNU cpio\)\s+(\S+)', output)
        return match.group(1) if match else None

    def flag_handler(self, name, flags):
        spec = self.spec

        if name == 'cflags':
            if '%intel@:17' in spec:
                flags.append('-no-gcc')

            elif '%clang' in spec or '%fj' in spec:
                flags.append('--rtlib=compiler-rt')

        return (flags, None, None)

    def configure_args(self):
        args=[]
        # See #31420 for discussion.
        # For %intel@19 comment out the conflict() above and uncomment
        # the next two lines.  Modify the path to point to a recent version
        # of gcc on your machine.  gcc@4.9.3 is known not to work.
        #if self.spec.satisfies('%intel@19'):
        #    args.append('CFLAGS=-gcc-name=/usr/tce/packages/gcc/gcc-10.2.1/bin/gcc')
        return args

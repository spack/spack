# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Cpio(AutotoolsPackage, GNUMirrorPackage):
    """GNU cpio copies files into or out of a cpio or tar archive. The
       archive can be another file on the disk, a magnetic tape, or a pipe.
    """
    homepage = "https://www.gnu.org/software/cpio/"
    gnu_mirror_path = "cpio/cpio-2.13.tar.gz"

    version('2.13', sha256='e87470d9c984317f658567c03bfefb6b0c829ff17dbf6b0de48d71a4c8f3db88')

    build_directory = 'spack-build'

    def flag_handler(self, name, flags):
        if self.spec.satisfies('%intel') and name == 'cflags':
            flags.append('-no-gcc')
        return (flags, None, None)

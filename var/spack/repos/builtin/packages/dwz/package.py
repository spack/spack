# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Dwz(MakefilePackage, SourcewarePackage):
    """DWZ: A DWARF optimization and duplicate removal tool"""

    homepage = "https://sourceware.org/dwz/"
    sourceware_mirror_path = "dwz/releases/dwz-0.14.tar.gz"
    git      = "git://sourceware.org/git/dwz.git"

    maintainers = ['iarspider']

    depends_on('elf')

    version('0.14-patches', branch='dwz-0.14-branch')
    version('0.14', sha256='33006eab875ff0a07f13fc885883c5bd9514d83ecea9f18bc46b5732dddf0d1f', preferred=True)

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install('dwz', prefix.bin)

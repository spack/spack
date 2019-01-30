# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Muscle(MakefilePackage):
    """MUSCLE is one of the best-performing multiple alignment programs
       according to published benchmark tests, with accuracy and speed
       that are consistently better than CLUSTALW."""

    homepage = "http://drive5.com/muscle/"
    url      = "http://www.drive5.com/muscle/muscle_src_3.8.1551.tar.gz"

    version('3.8.1551', '1b7c9661f275a82d3cf708f923736bf8')

    def edit(self, spec, prefix):
        makefile = FileFilter('Makefile')
        makefile.filter('-static', '')
        makefile.filter('-funroll-loops', '')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install('muscle', prefix.bin)

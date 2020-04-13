# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
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

    version('3.8.31', sha256='43c5966a82133bd7da5921e8142f2f592c2b5f53d802f0527a2801783af809ad',
            url='https://drive5.com/muscle/downloads3.8.31/muscle3.8.31_src.tar.gz')
    version('3.8.1551', sha256='c70c552231cd3289f1bad51c9bd174804c18bb3adcf47f501afec7a68f9c482e')

    @property
    def build_directory(self):
        if self.spec.satisfies('@3.8.31:'):
            return 'src'
        else:
            return '.'

    def edit(self, spec, prefix):
        target_name = 'mk' if self.spec.satisfies('@3.8.31:') else 'Makefile'
        makefile = FileFilter(join_path(self.build_directory, target_name))
        makefile.filter('-static', '')
        makefile.filter('-funroll-loops', '')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install('{0}/muscle'.format(self.build_directory), prefix.bin)

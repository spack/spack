# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Meraculous(CMakePackage):
    """Meraculous is a while genome assembler for Next Generation Sequencing
       data geared for large genomes."""

    homepage = "http://jgi.doe.gov/data-and-tools/meraculous/"
    url      = "https://downloads.sourceforge.net/project/meraculous20/Meraculous-v2.2.4.tar.gz"
    git      = "https://bitbucket.org/berkeleylab/genomics-meraculous2.git"

    version('2.2.5.1', branch='release-2.2.5.1')
    version('2.2.4', '349feb6cb178643a46e4b092c87bad3a')

    depends_on('perl', type=('build', 'run'))
    depends_on('boost@1.5.0:')
    depends_on('gnuplot@3.7:')
    depends_on('perl-log-log4perl', type=('build', 'run'))

    conflicts('%gcc@6.0.0:', when='@2.2.4')

    def patch(self):
        edit = FileFilter('CMakeLists.txt')
        edit.filter(r"-static-libstdc\+\+", "")

    def setup_environment(self, spack_env, run_env):
        run_env.set('MERACULOUS_ROOT', self.prefix)
        run_env.prepend_path('PERL5LIB', self.prefix.lib)

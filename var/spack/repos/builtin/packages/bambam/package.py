# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Bambam(MakefilePackage):
    """Bambam is a tool used to facilitate NGS analysis."""

    homepage = "http://udall-lab.byu.edu/Research/Software/BamBam"
    url      = "https://downloads.sourceforge.net/project/bambam/bambam-1.4.tgz"

    version('1.4', sha256='a9b178251d771aafb8c676d30a9af88ea2fc679c2a5672b515f86be0e69238f1')
    version('1.3', sha256='de91af03c1c09921a3a7f816b4df0564213e57c1a6024f2bcd63c0e8f0733a50', preferred=True)

    depends_on('perl', type=('build', 'run'))
    depends_on('samtools')
    depends_on('bamtools@2.3.0')
    depends_on('htslib')
    depends_on('zlib')

    def edit(self, spec, prefix):
        makefile = FileFilter('makefile')
        makefile.filter('INC = *', 'INC = -I%s ' %
                        self.spec['bamtools'].prefix.include)

    def install(self, spec, prefix):
        install_tree('bin', prefix.bin)
        install_tree('lib', prefix.lib)
        install_tree('scripts', prefix.scripts)

    def setup_environment(self, spack_env, run_env):
        spack_env.prepend_path('LIBRARY_PATH',
                               self.spec['samtools'].prefix.lib)
        spack_env.prepend_path('LIBRARY_PATH',
                               self.spec['bamtools'].prefix.lib)
        spack_env.prepend_path('LIBRARY_PATH',
                               self.spec['bamtools'].prefix.lib.bamtools)
        run_env.prepend_path('LD_LIBRARY_PATH',
                             self.spec['bamtools'].prefix.lib.bamtools)
        run_env.prepend_path('PATH', prefix.scripts)

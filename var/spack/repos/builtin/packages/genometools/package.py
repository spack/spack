# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Genometools(MakefilePackage):
    """genometools is a free collection of bioinformatics tools (in the realm
       of genome informatics) combined into a single binary named gt."""

    homepage = "http://genometools.org/"
    url      = "http://genometools.org/pub/genometools-1.5.9.tar.gz"

    version('1.5.9', 'e400d69092f9f13db09b33f9dea39d2e')

    depends_on('perl', type=('build', 'run'))
    depends_on('cairo')
    depends_on('pango')

    # build fails with gcc 7"
    conflicts('%gcc@7.1.0:')

    def install(self, spec, prefix):
        make('install', 'prefix=%s' % prefix)

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        spack_env.set('CPATH', self.prefix.include.genometools)

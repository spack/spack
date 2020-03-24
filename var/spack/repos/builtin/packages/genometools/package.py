# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Genometools(MakefilePackage):
    """genometools is a free collection of bioinformatics tools (in the realm
       of genome informatics) combined into a single binary named gt."""

    homepage = "http://genometools.org/"
    url      = "http://genometools.org/pub/genometools-1.5.9.tar.gz"

    version('1.6.1', sha256='528ca143a7f1d42af8614d60ea1e5518012913a23526d82e434f0dad2e2d863f',
            url="https://github.com/genometools/genometools/archive/v1.6.1.tar.gz")
    version('1.5.9', sha256='36923198a4214422886fd1425ef986bd7e558c73b94194982431cfd3dc7eb387')

    depends_on('perl', type=('build', 'run'))
    depends_on('cairo')
    depends_on('pango')

    # build fails with gcc 7"
    conflicts('%gcc@7.1.0:', when='@:1.5.9')

    def install(self, spec, prefix):
        make('install', 'prefix=%s' % prefix)

    def setup_dependent_build_environment(self, env, dependent_spec):
        env.set('CPATH', self.prefix.include.genometools)

# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Bamutil(MakefilePackage):
    """bamUtil is a repository that contains several programs
       that perform operations on SAM/BAM files. All of these programs
       are built into a single executable, bam.
    """

    homepage = "https://genome.sph.umich.edu/wiki/BamUtil"
    url      = "https://genome.sph.umich.edu/w/images/7/70/BamUtilLibStatGen.1.0.13.tgz"
    git      = "https://github.com/statgen/bamUtil.git"
    maintainers = ['snehring']

    version('1.0.15', commit='3ad3980a3a3a3fc35eca3636b7206676c8303ce6')
    version('1.0.13', sha256='16c1d01c37d1f98b98c144f3dd0fda6068c1902f06bd0989f36ce425eb0c592b')

    depends_on('zlib')
    depends_on('git', type='build', when='@1.0.15:')

    patch('libstatgen-issue-9.patch', when='@1.0.13')
    patch('libstatgen-issue-19.patch', when='@1.0.13')
    patch('libstatgen-issue-17.patch', when='@1.0.13')
    patch('libstatgen-issue-7.patch', when='@1.0.13')
    patch('verifybamid-issue-8.patch', when='@1.0.13')

    parallel = False

    @when('@1.0.15')
    def edit(self, spec, prefix):
        filter_file('git://', 'https://', 'Makefile.inc', String=True)

    @when('@1.0.15:')
    def build(self, spec, prefix):
        make('cloneLib')
        make()

    @property
    def install_targets(self):
        return ['install', 'INSTALLDIR={0}'.format(self.prefix.bin)]

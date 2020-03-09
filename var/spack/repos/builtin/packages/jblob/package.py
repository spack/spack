# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import fileinput, os, shutil

class Jblob(Package):
    """The German Climate Computing Center (DKRZ: Deutsches Klimarechenzentrum GmbH) 
       dsaprovides a Long Term Archiving Service for large research data sets which are relevant for climate or Earth system research.
    """

    homepage = "https://cera-www.dkrz.de/WDCC/ui/cerasearch"
    url      = "http://cera-www.dkrz.de/jblob/jblob-3.0.zip"

    maintainers = ['ajkotobi']

    version('3.0', sha256='576b5956358386a8832c6d1d13c410705e54888354a10cfd4f094513458067e4', expand=True)

    depends_on('openjdk@1.8.0_202-b08:', type=('build', 'link', 'run'))

    def setup_environment(self, spack_env, run_env):
        run_env.set('JAVA_HOME', self.spec['java'].prefix)

    def install(self, spec, prefix):

        with open('jblob') as f:
            replaced = f.read().replace('/opt/jblob-3.0', self.prefix)

        with open('jblob', "w") as f:
            f.write(replaced)

        mkdir(prefix.bin)
        copy('jblob', prefix.bin)
        install_tree('lib', prefix.lib)
        install_tree('docs', prefix.docs)

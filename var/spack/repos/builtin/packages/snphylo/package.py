# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Snphylo(Package):
    """A pipeline to generate a phylogenetic tree from huge SNP data"""

    homepage = "http://chibba.pgml.uga.edu/snphylo/"
    url      = "http://chibba.pgml.uga.edu/snphylo/snphylo.tar.gz"

    version('2016-02-04', '467660814965bc9bed6c020c05c0d3a6')

    depends_on('python', type=('build', 'run'))
    depends_on('r', type=('build', 'run'))
    depends_on('r-phangorn', type=('build', 'run'))
    depends_on('r-gdsfmt', type=('build', 'run'))
    depends_on('r-snprelate', type=('build', 'run'))
    depends_on('r-getopt', type=('build', 'run'))
    depends_on('muscle')
    depends_on('phylip')

    def install(self, spec, prefix):
        install_answer = ['y', 'y', 'y', 'y']
        install_answer_input = 'spack-config.in'
        with open(install_answer_input, 'w') as f:
            f.writelines(install_answer)
        with open(install_answer_input, 'r') as f:
            bash = which('bash')
            bash('./setup.sh', input=f)
            install_tree('.', prefix)

    def setup_environment(self, spack_env, run_env):
        run_env.prepend_path('PATH', self.spec.prefix)

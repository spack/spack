# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Interproscan(Package):
    """InterProScan is the software package that allows sequences
       (protein and nucleic) to be scanned against InterPro's signatures.
       Signatures are predictive models, provided by several different
       databases, that make up the InterPro consortium."""

    homepage = "https://www.ebi.ac.uk/interpro/interproscan.html"
    url      = "https://github.com/ebi-pf-team/interproscan/archive/5.36-75.0.tar.gz"

    version('5.36-75.0', sha256='383d7431e47c985056c856ceb6d4dcf7ed2559a4a3d5c210c01ce3975875addb')

    depends_on('java@8.0:8.9', type=('build', 'run'))
    depends_on('maven', type='build')
    depends_on('perl@5:', type=('build', 'run'))
    depends_on('python@3:', type=('build', 'run'))

    def install(self, spec, prefix):
        with working_dir('core'):
            which('mvn')('clean', 'install')

        install_tree('.', prefix)

        # link the main shell script into the PATH
        ips_bin_suffix = 'core/jms-implementation/target/interproscan-5-dist'
        symlink(join_path(prefix, ips_bin_suffix), prefix.bin)

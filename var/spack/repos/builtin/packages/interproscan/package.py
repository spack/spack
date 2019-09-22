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
    version('4.8',
            sha256='f1cb0ae1218eb05ed59ad7f94883f474eb9a6185a56ad3a93a364acb73506a3f',
            url='ftp://ftp.ebi.ac.uk/pub/software/unix/iprscan/4/RELEASE/4.8/iprscan_v4.8.tar.gz')

    resource(
        when='@:4.8',
        name='binaries',
        url="http://ftp.ebi.ac.uk/pub/databases/interpro/iprscan/BIN/4.x/iprscan_bin4.x_Linux64.tar.gz",
        sha256='551610a4682b112522f3ded5268f76ba9a47399a72e726fafb17cc938a50e7ee',
    )

    depends_on('java@8.0:8.9', when='@5:', type=('build', 'run'))
    depends_on('maven', when='@5:', type='build')
    depends_on('python@3:', when='@5:', type=('build', 'run'))
    depends_on('perl@5:', type=('build', 'run'))
    depends_on('perl-cgi', when='@:4.8', type=('build', 'run'))
    depends_on('perl-mailtools', when='@:4.8', type=('build', 'run'))
    depends_on('perl-xml-quote', when='@:4.8', type=('build', 'run'))
    depends_on('perl-xml-parser', when='@:4.8', type=('build', 'run'))
    depends_on('perl-io-string', when='@:4.8', type=('build', 'run'))
    depends_on('perl-io-stringy', when='@:4.8', type=('build', 'run'))

    patch('large-gid.patch', when='@5:')
    patch('non-interactive.patch', when='@:4.8')

    def install(self, spec, prefix):
        with working_dir('core'):
            which('mvn')('clean', 'install')

        install_tree('.', prefix)

        # link the main shell script into the PATH
        ips_bin_suffix = 'core/jms-implementation/target/interproscan-5-dist'
        symlink(join_path(prefix, ips_bin_suffix), prefix.bin)

    @when('@:4.8')
    def install(self, spec, prefix):
        perl = which('perl')

        src = join_path(self.stage.source_path, 'iprscan', 'bin', 'Linux')
        dst = join_path(self.stage.source_path, 'bin', 'binaries')
        force_symlink(src, dst)

        install_tree('.', prefix)

        with working_dir(prefix):
            perl('Config.pl')

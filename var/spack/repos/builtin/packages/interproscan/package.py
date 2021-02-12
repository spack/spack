# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
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

    version('5.50-84.0', sha256='d135b3d97eb3eb66d7068332bd9a6837bec7e7875b5bd8d9c48514b0013dc7b7')
    version('5.48-83.0', sha256='30a62d5c8097e7ff62f419ae68024fbe828b8fd75c34b1eba0af4f5fc7a7e15d')
    version('5.47-82.0', sha256='17bbf86d5a51569f21d75c01117e42376743405ec16e25937e71b03f2324f278')
    version('5.46-81.0', sha256='d96c97fb426510d6ccae83aa5a15dc35b1db65aea896e6666fa9aa32ee16c7fd')
    version('5.45-80.0', sha256='9aa89c9d7f07663e33b1346c082423510a6289bfbd86d765dc24bf0f180400d5')
    version('5.44-79.0', sha256='07f9445017a3aeeb8f1a32de00e29b93638e34bbf0de505dd73c52449dce3fb1')
    version('5.42-78.0', sha256='4658912043fb581dda6cb0b769ed0895f310d9ccc04725ebbeebfa2db4ac94d1')
    version('5.41-78.0', sha256='7813ff27a08b5f4a725d7a8e7a631ed86dcf6db502c4a3a894ec4853a186c746')
    version('5.40-77.0', sha256='699a6d456e9ac7243887e7469ed32b00b89578d8d6cbae03e70f08117fa3b751')
    version('5.39-77.0', sha256='d8c840139313379e039c729ecfe3c833f5ddb2672efa107324aef5fcc142f86d')
    version('5.38-76.0', sha256='cb191ff8eee275689b789167a57b368ea5c06bbcd36b4de23e8bbbbdc0fc7434')
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

    depends_on('java@8.0:8.9', type=('build', 'run'), when='@5:5.36-99.0')
    depends_on('java@11.0:', type=('build', 'run'), when='@5.37-76.0:')
    depends_on('maven', type='build', when='@5:')
    depends_on('perl@5:', type=('build', 'run'))
    depends_on('python@3:', when='@5:', type=('build', 'run'))
    depends_on('perl-cgi', when='@:4.8', type=('build', 'run'))
    depends_on('perl-mailtools', when='@:4.8', type=('build', 'run'))
    depends_on('perl-xml-quote', when='@:4.8', type=('build', 'run'))
    depends_on('perl-xml-parser', when='@:4.8', type=('build', 'run'))
    depends_on('perl-io-string', when='@:4.8', type=('build', 'run'))
    depends_on('perl-io-stringy', when='@:4.8', type=('build', 'run'))

    patch('large-gid.patch', when='@5:')
    patch('non-interactive.patch', when='@:4.8')
    patch('ps_scan.patch', when='@:4.8')

    def install(self, spec, prefix):
        with working_dir('core'):
            if self.run_tests:
                which('mvn')('verify')
            else:
                which('mvn')('package', '-DskipTests')

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

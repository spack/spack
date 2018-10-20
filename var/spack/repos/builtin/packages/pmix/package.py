# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *
import spack.architecture


class Pmix(AutotoolsPackage):
    """The Process Management Interface (PMI) has been used for quite some time
       as a means of exchanging wireup information needed for interprocess
       communication. Two versions (PMI-1 and PMI-2) have been released as part
       of the MPICH effort. While PMI-2 demonstrates better scaling properties
       than its PMI-1 predecessor, attaining rapid launch and wireup of the
       roughly 1M processes executing across 100k nodes expected for exascale
       operations remains challenging.  PMI Exascale (PMIx) represents an
        attempt to resolve these questions by providing an extended version
       of the PMI definitions specifically designed to support clusters up
       to and including exascale sizes.  The overall objective of the project
       is not to branch the existing definitions - in fact, PMIx fully
       supports both of the existing PMI-1 and PMI-2 APIs - but rather to
       (a) augment and extend those APIs to eliminate some current restrictions
       that impact scalability, (b) establish a standards-like body for
       maintaining the definitions, and (c) provide a reference implementation
       of the PMIx standard that demonstrates the desired level of
       scalability."""

    homepage = "https://pmix.github.io/pmix"
    url      = "https://github.com/pmix/pmix/releases/download/v2.0.1/pmix-2.0.1.tar.bz2"

    version('3.0.2',    sha256='df68f35a3ed9517eeade80b13855cebad8fde2772b36a3f6be87559b6d430670')
    version('3.0.1',    sha256='b81055d2c0d61ef5a451b63debc39c820bcd530490e2e4dcb4cdbacb618c157c')
    version('3.0.0',    sha256='ee8f68107c24b706237a53333d832445315ae37de6773c5413d7fda415a6e2ee')
    version('2.1.4',    sha256='eb72d292e76e200f02cf162a477eecea2559ef3ac2edf50ee95b3fe3983d033e')
    version('2.1.3',    sha256='281283133498e7e5999ed5c6557542c22408bc9eb51ecbcf7696160616782a41')
    version('2.1.2',    sha256='94bb9c801c51a6caa1b8cef2b85ecf67703a5dfa4d79262e6668c37c744bb643')
    version('2.0.1',    'ba3193b485843516e6b4e8641e443b1e')
    version('2.0.0',    '3e047c2ea0ba8ee9925ed92b205fd92e')
    version('1.2.5',    'c3d20cd9d365a813dc367afdf0f41c37')
    version('1.2.4',    '242a812e206e7c5948f1f5c9688eb2a7')
    version('1.2.3',    '102b1cc650018b62348b45d572b158e9')
    version('1.2.2',    'd85c8fd437bd88f984549425ad369e9f')
    version('1.2.1',    'f090f524681c52001ea2db3b0285596f')
    version('1.2.0',    '6a42472d5a32e1c31ce5da19d50fc21a')

    depends_on('libevent')

    def configure_args(self):

        spec = self.spec
        config_args = [
            '--enable-shared',
            '--enable-static'
        ]

        # external libevent support (needed to keep Open MPI happy)
        config_args.append(
            '--with-libevent={0}'.format(spec['libevent'].prefix))

        # Versions < 2.1.1 have a bug in the test code that *sometimes*
        # causes problems on strict alignment architectures such as
        # aarch64.  Work-around is to just not build the test code.
        if 'aarch64' in spack.architecture.sys_type() and \
           self.spec.version < Version('2.1.1'):
            config_args.append('--without-tests-examples')

        return config_args

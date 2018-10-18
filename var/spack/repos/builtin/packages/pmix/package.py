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

    version('3.0.2',    'dc2e501605dde93ab459a5e060e01500')
    version('3.0.1',    'ffe6bc08ab600173ea6e7d4509777629')
    version('3.0.0',    '396969979a36d45bd292908e4bcec5c8')
    version('2.1.4',    'edcfd7d1e2c2bcbb3e9852b66b57120e')
    version('2.1.3',    '9320a4f3aef305fab4f7ac3520153160')
    version('2.1.2',    '9f99fd893be49c2cb0cd8926cf6fcc78')
    version('2.1.1',    'f9f109421661b757245d5e0bd44a38b3')
    version('2.1.0',    'fc97513b601d78fe7c6bb20c6a21df3c')
    version('2.0.3',    'fae199c9fa1d1f1bc20c336f1292f950')
    version('2.0.2',    'e3ed1deed87c84f9b43da2621c6ad689')
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

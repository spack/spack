# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlSoapLite(PerlPackage):
    """Perl's Web Services Toolkit"""

    homepage = "http://search.cpan.org/~phred/SOAP-Lite-1.20/lib/SOAP/Lite.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/P/PH/PHRED/SOAP-Lite-1.22.tar.gz"

    version('1.22', '86c31341311498a08c6309e62168f655')

    depends_on('perl-io-sessiondata', type=('build', 'run'))
    depends_on('perl-lwp-protocol-https', type=('build', 'run'))
    depends_on('perl-task-weaken', type=('build', 'run'))
    depends_on('perl-xml-parser-lite', type=('build', 'run'))
    depends_on('perl-xml-parser', type=('build', 'run'))
    depends_on('perl-test-warn', type=('build', 'run'))
    depends_on('perl-class-inspector', type=('build', 'run'))

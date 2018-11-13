# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import inspect


class PerlNetSsleay(PerlPackage):
    """Perl extension for using OpenSSL"""

    homepage = "http://search.cpan.org/~mikem/Net-SSLeay-1.82/lib/Net/SSLeay.pod"
    url      = "http://search.cpan.org/CPAN/authors/id/M/MI/MIKEM/Net-SSLeay-1.82.tar.gz"

    version('1.82', '2170469d929d5173bacffd0cb2d7fafa')

    depends_on('openssl')

    def configure(self, spec, prefix):
        self.build_method = 'Makefile.PL'
        self.build_executable = inspect.getmodule(self).make
        # Do you want to run external tests?
        config_answers = ['\n']
        config_answers_filename = 'spack-config.in'

        with open(config_answers_filename, 'w') as f:
            f.writelines(config_answers)

        with open(config_answers_filename, 'r') as f:
            inspect.getmodule(self).perl('Makefile.PL', 'INSTALL_BASE={0}'.
                                         format(prefix), 'OPENSSL_PREFIX=%s' %
                                         self.spec['openssl'].prefix, input=f)

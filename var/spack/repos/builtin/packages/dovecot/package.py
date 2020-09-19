# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Dovecot(AutotoolsPackage):
    """Dovecot mail server."""

    homepage = "https://github.com/dovecot/core"
    url      = "https://github.com/dovecot/core/archive/2.3.11.3.tar.gz"

    version('2.3.11.3', sha256='a76d321dc36dfcf172bede5c8b0cc201b8ff3911c5d8edf3db75e74c62a42992')

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
    depends_on('m4',       type='build')
    depends_on('gettext')

    def setup_build_environment(self, env):
        aclocal_path = self.spec['gettext'].prefix.share.aclocal
        env.prepend_path('ACLOCAL_PATH', aclocal_path)

    def autoreconf(self, spec, prefix):
        bash = which('bash')
        bash('./autogen.sh')

    def configure_args(self):
        args = ['PANDOC=false']
        return args

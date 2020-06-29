# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Bmake(Package):
    """Portable version of NetBSD make(1)."""

    homepage = "http://www.crufty.net/help/sjg/bmake.htm"
    url      = "http://www.crufty.net/ftp/pub/sjg/bmake-20180512.tar.gz"

    version('20180512', sha256='ac3cd262065fcc20c1dec7c95f06306c8138b3e17025b949343a06a8980a5508')
    version('20171207', sha256='1703667e53a0498c0903b20612ebcbb41b886a94b238624cfeadd91a4111d39a')

    phases = ['configure', 'build', 'install']

    def patch(self):
        # Do not pre-roff cat pages
        filter_file('MANTARGET?', 'MANTARGET', 'mk/man.mk', string=True)

    def configure(self, spec, prefix):
        sh = which('sh')
        sh('boot-strap', 'op=configure')

    def build(self, spec, prefix):
        sh = which('sh')
        sh('boot-strap', 'op=build')

    def install(self, spec, prefix):
        sh = which('sh')
        sh('boot-strap', '--prefix={0}'.format(prefix), 'op=install')

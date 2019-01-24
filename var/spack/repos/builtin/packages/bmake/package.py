# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Bmake(Package):
    """Portable version of NetBSD make(1)."""

    homepage = "http://www.crufty.net/help/sjg/bmake.htm"
    url      = "http://www.crufty.net/ftp/pub/sjg/bmake-20180512.tar.gz"

    version('20180512', '48ba5933833a7f224d76ce482eedfec0')
    version('20171207', '5d7f2f85f16c4a6ba34ceea68957447f')

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

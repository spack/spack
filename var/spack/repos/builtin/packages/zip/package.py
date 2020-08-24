# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Zip(MakefilePackage):
    """Zip is a compression and file packaging/archive utility."""

    homepage = 'http://www.info-zip.org/Zip.html'
    url      = 'http://downloads.sourceforge.net/infozip/zip30.tar.gz'

    version('3.0', sha256='f0e8bb1f9b7eb0b01285495a2699df3a4b766784c1765a8f1aeedf63c0806369')

    depends_on('bzip2')

    def url_for_version(self, version):
        return 'http://downloads.sourceforge.net/infozip/zip{0}.tar.gz'.format(version.joined)

    make_args = ['-f', 'unix/Makefile']
    build_targets = make_args + ['generic']

    @property
    def install_targets(self):
        return self.make_args + ['prefix={0}'.format(self.prefix), 'install']

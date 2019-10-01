# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Unzip(MakefilePackage):
    """Unzip is a compression and file packaging/archive utility."""

    homepage = 'http://www.info-zip.org/Zip.html'
    url      = 'http://downloads.sourceforge.net/infozip/unzip60.tar.gz'

    version('6.0', '62b490407489521db863b523a7f86375')

    # The Cray cc wrapper doesn't handle the '-s' flag (strip) cleanly.
    @when('platform=cray')
    def patch(self):
        filter_file(r'^LFLAGS2=.*', 'LFLAGS2=', join_path('unix', 'configure'))

    make_args = ['-f', join_path('unix', 'Makefile')]
    build_targets = make_args + ['generic']

    def url_for_version(self, version):
        return 'http://downloads.sourceforge.net/infozip/unzip{0}.tar.gz'.format(version.joined)

    @property
    def install_targets(self):
        return self.make_args + ['prefix={0}'.format(self.prefix), 'install']

# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Umoci(MakefilePackage):
    """umoci modifies Open Container images, intending to be a
    complete manipulation tool for OCI images."""

    homepage = "https://umo.ci/"
    url      = "https://github.com/openSUSE/umoci/archive/v0.4.4.tar.gz"

    version('0.4.4', expand=False,
            sha256='bc5c53812e0076d026aa275b197b878857cf7ba7a4f048fd13433de6107b9aed')
    version('0.4.3', expand=False,
            sha256='b7d537fec84d4327b1bbfe27118f69df5591143a74a7a1b66cc9904d85c30226')
    version('0.4.2', expand=False,
            sha256='fbc397dd39bda2570155dc3b1be0835809a36fccc342e2545b3edb9f0f9dc6f5')
    version('0.4.1', expand=False,
            sha256='0d83e01167383f529d726e9fd455660d4837371d5f0d82fad405f3ae6ae52486')
    version('0.4.0', expand=False,
            sha256='66997e270dee8abc9796385b162a1e8e32dd2ee2359e5200af4e6671cc1e76a0')

    depends_on('go')

    def install(self, spec, prefix):
        mkdirp(join_path(self.stage.source_path,
               'src', 'github.com', 'openSUSE', 'umoci'))

        with working_dir(join_path('src', 'github.com', 'openSUSE', 'umoci')):
            tar = which('tar')
            tar('zxf', self.stage.archive_file, '--strip-components=1')
            make('GOPATH={0}'.format(self.stage.source_path))
            make('PREFIX=', 'DESTDIR={0}'.format(prefix), 'install')

# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os


class Hub(Package):
    """The github git wrapper"""

    homepage = "https://github.com/github/hub"
    url      = "https://github.com/github/hub/archive/v2.2.3.tar.gz"
    git      = "https://github.com/github/hub.git"

    version('head', branch='master')
    version('2.2.3', '6675992ddd16d186eac7ba4484d57f5b')
    version('2.2.2', '7edc8f5b5d3c7c392ee191dd999596fc')
    version('2.2.1', '889a31ee9d10ae9cb333480d8dbe881f')
    version('2.2.0', 'eddce830a079b8480f104aa7496f46fe')
    version('1.12.4', '4f2ebb14834c9981b04e40b0d1754717')

    extends("go")

    def install(self, spec, prefix):
        env = os.environ
        env['GOPATH'] = self.stage.source_path + ':' + env['GOPATH']
        bash = which('bash')
        bash(os.path.join('script', 'build'), '-o', os.path.join(prefix, 'bin',
                                                                 'hub'))

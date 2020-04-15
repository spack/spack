# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class CodeServer(Package):
    """code-server is VS Code running on a remote server,
    accessible through the browser."""

    homepage = "https://github.com/cdr/code-server"
    url      = "https://github.com/cdr/code-server/releases/download/3.1.0/code-server-3.1.0-linux-x86_64.tar.gz"

    version('3.1.0', sha256='5ef85c8f280ce781a176a8b77386b333efe892755a5c325a1782e4eac6016e59')

    # FIXME: Add dependencies if required.
    # depends_on('foo')

    def install(self, spec, prefix):
        ln = which('ln')
        mkdir = which('mkdir')
        cp = which('cp')

        cp('-r', '{0}/.'.format(self.stage.source_path), prefix)
        mkdir(prefix.bin)
        ln('-s', '{0}/code-server'.format(prefix), prefix.bin) 

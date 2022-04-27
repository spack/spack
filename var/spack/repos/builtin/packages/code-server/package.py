# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class CodeServer(Package):
    """code-server is VS Code running on a remote server,
    accessible through the browser."""

    homepage = "https://github.com/cdr/code-server"

    version('3.12.0', sha256='d3ca41a55e36d73d80300702af2687e25d440cff6b613bb58a2c88d9b8a0a38f')
    version('3.9.3', sha256='eba42eaf868c2144795b1ac54929e3b252ae35403bf8553b3412a5ac4f365a41')
    version('3.4.1', sha256='afdb89f4dc7201c03cb35d4f8dc1ccb6060bd0da324a6789089de264d3406817')
    version('3.1.1', sha256='5dd922d28b2e351c146081849d987fb1e439ee7d53b941434b2eecb2a194da71')
    version('3.1.0', sha256='5ef85c8f280ce781a176a8b77386b333efe892755a5c325a1782e4eac6016e59')

    depends_on('git@2:')

    def url_for_version(self, version):

        if version <= Version('3.2.0'):
            url = "https://github.com/cdr/code-server/releases/download/v{}/code-server-{}-linux-x86_64.tar.gz"
        else:
            url = "https://github.com/cdr/code-server/releases/download/v{}/code-server-{}-linux-amd64.tar.gz"

        return url.format(version, version)

    def install(self, spec, prefix):
        install_tree('.', prefix)

        if spec.version <= Version('3.1.1'):
            mkdir(prefix.bin)
            symlink('{0}/code-server'.format(prefix),
                    '{0}/code-server'.format(prefix.bin))

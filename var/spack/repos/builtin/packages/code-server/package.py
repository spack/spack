# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install code-server
#
# You can edit this file again by typing:
#
#     spack edit code-server
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class CodeServer(Package):
    """code-server is VS Code running on a remote server,
    accessible through the browser."""

    homepage = "https://github.com/cdr/code-server"
    url      = "https://github.com/cdr/code-server/releases/download/3.1.0/code-server-3.1.0-linux-x86_64.tar.gz"

    # FIXME: Add a list of GitHub accounts to
    # notify when the package is updated.
    # maintainers = ['github_user1', 'github_user2']

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

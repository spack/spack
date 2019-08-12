# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class BashCompletion(AutotoolsPackage):
    """Programmable completion functions for bash."""

    homepage = "https://github.com/scop/bash-completion"
    url      = "https://github.com/scop/bash-completion/archive/2.3.tar.gz"
    git      = "https://github.com/scop/bash-completion.git"

    version('develop', branch='master')
    version('2.7', 'f72c9e2e877d188c3159956a3496a450e7279b76')
    version('2.3', '67e50f5f3c804350b43f2b664c33dde811d24292')

    # Build dependencies
    depends_on('automake', type='build')
    depends_on('autoconf', type='build')
    depends_on('libtool',  type='build')

    # Other dependencies
    depends_on('bash@4.1:', type='run')

    @run_before('install')
    def create_install_directory(self):
        mkdirp(join_path(self.prefix.share, 'bash-completion', 'completions'))

    @run_after('install')
    def show_message_to_user(self):
        prefix = self.prefix
        # Guidelines for individual user as provided by the author at
        # https://github.com/scop/bash-completion
        print('=====================================================')
        print('Bash completion has been installed. To use it, please')
        print('include the following lines in your ~/.bash_profile :')
        print('')
        print('# Use bash-completion, if available')
        print('[[ $PS1 && -f %s/share/bash-completion/bash_completion ]] && \ ' % prefix)  # NOQA: ignore=E501
        print('    . %s/share/bash-completion/bash_completion' % prefix)
        print('')
        print('=====================================================')

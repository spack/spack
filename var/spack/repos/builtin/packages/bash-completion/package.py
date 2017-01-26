##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *


class BashCompletion(AutotoolsPackage):
    """Programmable completion functions for bash."""
    homepage = "https://github.com/scop/bash-completion"
    url = "https://github.com/scop/bash-completion/archive/2.3.tar.gz"

    version('2.3', '67e50f5f3c804350b43f2b664c33dde811d24292')
    version('develop',  git='https://github.com/scop/bash-completion.git')

    # Build dependencies
    depends_on('automake', type='build')
    depends_on('autoconf', type='build')
    depends_on('libtool',  type='build')

    # Other dependencies
    depends_on('bash@4.1:', type='run')

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

##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
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
from glob import glob


class AsperaCli(Package):
    """The Aspera CLI client for the Fast and Secure Protocol (FASP)."""

    homepage = "https://asperasoft.com"
    url      = "https://download.asperasoft.com/download/sw/cli/3.7.7/aspera-cli-3.7.7.608.927cce8-linux-64-release.sh"

    version('3.7.7', 'e92140d809e7e65112a5d1cd49c442cf',
            url='https://download.asperasoft.com/download/sw/cli/3.7.7/aspera-cli-3.7.7.608.927cce8-linux-64-release.sh',
            expand=False)

    def setup_environment(self, spack_env, run_env):
        run_env.prepend_path('PATH', self.prefix.cli.bin)

    def install(self, spec, prefix):
        runfile = glob(join_path(self.stage.path, 'aspera-cli*.sh'))[0]
        # Update destination path
        filter_file('INSTALL_DIR=~/.aspera',
                    'INSTALL_DIR=%s' % prefix,
                    runfile,
                    string=True)
        # Install
        chmod = which('chmod')
        chmod('+x', runfile)
        runfile = which(runfile)
        runfile()

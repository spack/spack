# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

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
        runfile = glob(join_path(self.stage.source_path, 'aspera-cli*.sh'))[0]
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

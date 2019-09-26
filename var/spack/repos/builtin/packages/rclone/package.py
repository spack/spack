# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Rclone(Package):
    """Rclone is a command line program to sync files and directories
       to and from various cloud storage providers"""

    homepage = "http://rclone.org"
    url      = "https://github.com/ncw/rclone/releases/download/v1.43/rclone-v1.43.tar.gz"

    version('1.43', sha256='d30527b00cecb4e5e7188dddb78e5cec62d67cf2422dab82190db58512b5a4e3')

    depends_on("go", type='build')

    def setup_environment(self, spack_env, run_env):
        # Point GOPATH at the top of the staging dir for the build step.
        spack_env.prepend_path('GOPATH', self.stage.path)

    def install(self, spec, prefix):
        go('build')
        mkdirp(prefix.bin)
        install('rclone', prefix.bin)

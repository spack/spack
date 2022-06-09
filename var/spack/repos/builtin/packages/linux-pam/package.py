# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class LinuxPam(AutotoolsPackage):
    """Linux PAM (Pluggable Authentication Modules for Linux) project."""

    homepage = "http://www.linux-pam.org/"
    url      = "https://github.com/linux-pam/linux-pam/releases/download/v1.5.2/Linux-PAM-1.5.2.tar.xz"

    version('1.5.1', sha256='201d40730b1135b1b3cdea09f2c28ac634d73181ccd0172ceddee3649c5792fc')
    version('1.5.2', sha256='e4ec7131a91da44512574268f493c6d8ca105c87091691b8e9b56ca685d4f94d')
    version('1.5.0', sha256='02d39854b508fae9dc713f7733bbcdadbe17b50de965aedddd65bcb6cc7852c8')
    version('1.4.0', sha256='cd6d928c51e64139be3bdb38692c68183a509b83d4f2c221024ccd4bcddfd034')
    version('1.3.1', sha256='eff47a4ecd833fbf18de9686632a70ee8d0794b79aecb217ebd0ce11db4cd0db')

    depends_on('m4',       type='build')
    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')

    def configure_args(self):
        config_args = [
            '--includedir=' + self.prefix.include.security
        ]
        return config_args

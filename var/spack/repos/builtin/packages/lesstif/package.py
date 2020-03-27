# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Lesstif(AutotoolsPackage):
    """LessTif is the Hungry Programmers' version of OSF/Motif."""

    homepage = "https://sourceforge.net/projects/lesstif"
    url      = "https://sourceforge.net/projects/lesstif/files/lesstif/0.95.2/lesstif-0.95.2.tar.bz2/download"

    version('0.95.2', sha256='eb4aa38858c29a4a3bcf605cfe7d91ca41f4522d78d770f69721e6e3a4ecf7e3')

    depends_on('libice')
    depends_on('libsm')
    depends_on('libxt')

    def setup_build_environment(self, env):
        env.set('DESTDIR', self.prefix)

    def configure_args(self):
        args = [
            '--prefix='
        ]
        return args

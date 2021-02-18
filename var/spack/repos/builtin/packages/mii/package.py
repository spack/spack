# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Mii(MakefilePackage):
    """Mii is an inverted indexing system for environment modules.
       After installation you will no longer need to load modules to run
       applications.

       NOTE: Additional steps are required after installing the
       Spack package to enable Mii in your shell. Please see the README
       on the homepage for more information."""

    homepage = "https://github.com/codeandkey/mii"
    url      = "https://github.com/codeandkey/mii/archive/1.0.2.tar.gz"

    version('1.0.4', sha256='3c4e7e6e8c21969da8dade05fecab35be61f2bb82d75eeaf19db8cc97f8058b5')
    version('1.0.3', sha256='9b5a0e4e0961cf848677ed61b4f6c03e6a443f8592ed668d1afea302314b47a8')
    version('1.0.2', sha256='1c2c86ec37779ecd3821c30ce5b6dd19be4ec1813da41832d49ff3dcf615e22d')

    def url_for_version(self, version):
        url = 'https://github.com/codeandkey/mii/archive/'
        if version >= Version('1.0.4'):
            url += 'v' + str(version) + '.tar.gz'
        else:
            url += str(version) + '.tar.gz'
        return url

    def setup_build_environment(self, env):
        env.set('PREFIX', self.prefix)

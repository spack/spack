# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class QtCreator(QMakePackage):
    """The Qt Creator IDE."""
    homepage = 'https://www.qt.io/ide/'
    url      = 'http://download.qt.io/official_releases/qtcreator/4.3/4.3.1/qt-creator-opensource-src-4.3.1.tar.gz'

    list_url = 'http://download.qt.io/official_releases/qtcreator/'
    list_depth = 2

    version('4.4.0', 'bae2e08bb5087aba65d41eb3f9328d9a')
    version('4.3.1', '6769ea47f287e2d9e30ff92acb899eef')
    version('4.1.0', '657727e4209befa4bf5889dff62d9e0a')

    depends_on('qt@5.6.0:+opengl')
    # Qt Creator comes bundled with its own copy of sqlite. Qt has a build
    # dependency on Python, which has a dependency on sqlite. If Python is
    # built with a different version of sqlite than the bundled copy, it will
    # cause symbol conflict. Force Spack to build with the same version of
    # sqlite as the bundled copy.
    depends_on('sqlite@3.8.10.2')

    # Qt Creator 4.3.0+ requires a C++14 compiler
    conflicts('%gcc@:4.8', when='@4.3.0:')

    def url_for_version(self, version):
        url = 'http://download.qt.io/official_releases/qtcreator/{0}/{1}/qt-creator-opensource-src-{1}.tar.gz'
        return url.format(version.up_to(2), version)

    def setup_environment(self, spack_env, run_env):
        spack_env.set('INSTALL_ROOT', self.prefix)

    def qmake_args(self):
        return ['-r']

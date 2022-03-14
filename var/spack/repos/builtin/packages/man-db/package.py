# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class ManDb(AutotoolsPackage):
    """man-db is an implementation of the standard Unix
    documentation system accessed using the man command. It uses
    a Berkeley DB database in place of the traditional
    flat-text whatis databases."""

    homepage = "https://www.nongnu.org/man-db/"
    git      = "https://gitlab.com/cjwatson/man-db"
    url      = "https://download.savannah.nongnu.org/releases/man-db/man-db-2.10.1.tar.xz"

    version('2.10.1', sha256='2ffd8f2e80122fe72e60c740c851e6a3e15c9a7921185eb4752c1c672824bed6')
    version('2.7.6.1', sha256='08edbc52f24aca3eebac429b5444efd48b9b90b9b84ca0ed5507e5c13ed10f3f')

    depends_on('pkgconf', type='build')
    depends_on('gettext')
    depends_on('libpipeline@1.5.0:', when='@2.8.0:')
    depends_on('libpipeline@1.4.0:', when='@2.7.1:')
    depends_on('libpipeline@1.3.0:', when='@2.6.7:')
    depends_on('libpipeline@1.1.0:', when='@2.6.0:')
    depends_on('flex')
    depends_on('gdbm')
    depends_on('groff', type=('build', 'link', 'run'))

    # TODO: add gzip support via a new package.
    # man pages are typically compressed, include all available
    # compression libraries
    depends_on('bzip2', type=('build', 'link', 'run'))
    depends_on('xz',    type=('build', 'link', 'run'))

    def configure_args(self):
        args = [
            '--disable-setuid',
            # defaults to a location that needs root privs to write in
            '--with-systemdtmpfilesdir={0}/tmp'.format(self.prefix)
        ]
        return args

    def install(self, spec, prefix):
        make('install', 'DESTDIR=%s' % prefix)

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
    url      = "https://git.savannah.nongnu.org/cgit/man-db.git/snapshot/man-db-2.7.6.1.tar.gz"

    version('2.7.6.1', sha256='dd913662e341fc01e6721878b6cbe1001886cc3bfa6632b095937bba3238c779')

    # When not using views, it is easy to go over the default limit
    # of 128 directories in MANPATH when doing spack installation.
    # The following variant allows to increase the limit
    # in order to avoid an error when using man.
    variant('maxdirs', default='1024', values=('128', '1024'),
            description="Compile time definition of the maximum number of manual page"
                        " hierarchies expected in the manpath.")

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('pkgconf', type='build')
    depends_on('gettext')
    depends_on('libpipeline')
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

    def patch(self):
        filter_file(r'\#define MAXDIRS 128',
                    '#define MAXDIRS %s' % self.spec.variants['maxdirs'].value,
                    'include/manconfig.h.in')

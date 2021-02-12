# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class SkilionOnedrive(MakefilePackage):
    """A complete tool to interact with OneDrive on Linux,
    developed by Skilion, following the UNIX philosophy."""

    homepage = "https://github.com/skilion/onedrive"
    url      = "https://github.com/skilion/onedrive/archive/v1.1.1.tar.gz"

    version('1.1.4', sha256='c6ef18c5798ce70c32843f2bed73600af5ad342fd20239c973887e9e751a35b6')
    version('1.1.3', sha256='fb12235a73919b3374b8f27785b834a690fba1c6e70c6e6f1f5da3e51eb471a0')
    version('1.1.2', sha256='d68588bf8bc3700a06243db675cc672f94530cbfd6571a0a51da473fb5449309')
    version('1.1.1', sha256='fb51c81ec95c28f3fe3b29e3b7f915e30161bd5f4b14bb53ae5c2233cc1e92e9')

    depends_on('dmd')
    depends_on('curl')
    depends_on('sqlite')

    def edit(self, spec, prefix):
        makefile = FileFilter('Makefile')
        # Generate the version file
        makefile.filter('.git/HEAD .git/index', '', string=True)
        makefile.filter('$(shell git describe --tags)',
                        '{0}'.format(spec.version),
                        string=True)
        # Patch sqlite.d https://github.com/skilion/onedrive/issues/392
        sqlited = FileFilter('src/sqlite.d')
        sqlited.filter('std.c.stdlib', 'core.stdc.stdlib', String=True)

    def build(self, spec, prefix):
        make('onedrive', 'DESTDIR={0}'.format(prefix), 'PREFIX=/')

    def install(self, spec, prefix):
        make('install', 'DESTDIR={0}'.format(prefix), 'PREFIX=/')

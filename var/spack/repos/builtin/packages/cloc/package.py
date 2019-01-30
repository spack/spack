# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Cloc(Package):
    """Count, or compute differences of, physical lines of source code in the
    given files (may be archives such as compressed tarballs or zip files)
    and/or recursively below the given directories."""
    homepage = "https://github.com/AlDanial/cloc/"
    url      = "https://github.com/AlDanial/cloc/releases/download/1.74/cloc-1.74.tar.gz"

    version('1.74', '1372da13a83862c186aa0b6b0c9b86f5')

    depends_on('perl')

    def install(self, spec, prefix):
        # rewrite the script's #! line to call the perl dependency
        shbang = '#!' + spec['perl'].command.path
        filter_file(r'^#!/usr/bin/env perl', shbang, 'cloc')
        filter_file(r'^#!/usr/bin/env perl', shbang, 'sqlite_formatter')

        # cloc doesn't have a build system. We have to do our own install here.
        mkdirp(prefix.bin)
        install('cloc', join_path(prefix.bin, "cloc"))
        install('sqlite_formatter', join_path(prefix.bin, "sqlite_formatter"))
        install('./LICENSE', "%s" % prefix)
        install('./README.md', "%s" % prefix)

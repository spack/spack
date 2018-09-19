##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
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

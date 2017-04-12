##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
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
import glob
from spack import *


class Leveldb(Package):
    """LevelDB is a fast key-value storage library written at Google
    that provides an ordered mapping from string keys to string values."""

    homepage = "https://github.com/google/leveldb"
    url      = "https://github.com/google/leveldb/archive/v1.20.tar.gz"

    version('1.20', '298b5bddf12c675d6345784261302252')
    version('1.18', '73770de34a2a5ab34498d2e05b2b7fa0')

    depends_on("snappy")

    def install(self, spec, prefix):
        make()

        mkdirp(prefix.include)
        mkdirp(prefix.lib)
        mkdirp(join_path(prefix.lib, 'pkgconfig'))

        cp = which('cp')

        # cp --preserve=links libleveldb.* prefix/lib
        args = glob.glob('out-shared/libleveldb.*') \
            + glob.glob('out-static/libleveldb.*')
        args.append(prefix.lib)
        cp('--preserve=links', *args)

        cp('-r', 'include/leveldb', prefix.include)

        with open(join_path(prefix.lib, 'pkgconfig', 'leveldb.pc'), 'w') as f:
            f.write('prefix={0}\n'.format(prefix))
            f.write('exec_prefix=${prefix}\n')
            f.write('libdir={0}\n'.format(prefix.lib))
            f.write('includedir={0}\n'.format(prefix.include))
            f.write('\n')
            f.write('Name: leveldb\n')
            f.write('Description: LevelDB is a fast key-value storage library'
                    ' written at Google that provides an ordered mapping from'
                    ' string keys to string values.\n')
            f.write('Version: {0}\n'.format(spec.version))
            f.write('Cflags: -I${includedir}\n')
            f.write('Libs: -L${libdir} -lleveldb\n')

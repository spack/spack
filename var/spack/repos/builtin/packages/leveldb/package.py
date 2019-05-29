# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import glob
from spack import *


class Leveldb(MakefilePackage):
    """LevelDB is a fast key-value storage library written at Google
    that provides an ordered mapping from string keys to string values."""

    homepage = "https://github.com/google/leveldb"
    url      = "https://github.com/google/leveldb/archive/v1.20.tar.gz"
    git      = "https://github.com/google/leveldb.git"

    version('master', branch='master')
    version('1.20', '298b5bddf12c675d6345784261302252')
    version('1.18', '73770de34a2a5ab34498d2e05b2b7fa0')

    depends_on("snappy")

    def install(self, spec, prefix):
        mkdirp(prefix.lib.pkgconfig)

        libraries  = glob.glob('out-shared/libleveldb.*')
        libraries += glob.glob('out-static/libleveldb.*')
        for library in libraries:
            install(library, prefix.lib)

        install_tree('include', prefix.include)

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

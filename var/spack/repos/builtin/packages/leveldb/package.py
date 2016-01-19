import os
import glob
from spack import *

class Leveldb(Package):
    """LevelDB is a fast key-value storage library written at Google
    that provides an ordered mapping from string keys to string values."""

    homepage = "https://github.com/google/leveldb"
    url      = "https://github.com/google/leveldb/archive/v1.18.tar.gz"

    version('1.18', '73770de34a2a5ab34498d2e05b2b7fa0')

    depends_on("snappy")

    def install(self, spec, prefix):
        make()

        mkdirp(prefix.include)
        mkdirp(prefix.lib)

        cp = which('cp')

        # cp --preserve=links libleveldb.* prefix/lib
        args = glob.glob('libleveldb.*')
        args.append(prefix + '/lib')
        cp('--preserve=links', *args)

        cp('-r', 'include/leveldb', prefix + '/include')

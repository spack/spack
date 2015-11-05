import os
from spack import *

class Lmdb(Package):
    """Read-only mirror of official repo on openldap.org. Issues and
    pull requests here are ignored. Use OpenLDAP ITS for issues.
    http://www.openldap.org/software/repo.html"""


    homepage = "http://www.openldap.org/software/repo.html"
    url      = "https://github.com/LMDB/lmdb/archive/LMDB_0.9.16.tar.gz"

    version('0.9.16', '0de89730b8f3f5711c2b3a4ba517b648')

    def install(self, spec, prefix):
        os.chdir('libraries/liblmdb')

        make()

        mkdirp(prefix.bin)
        mkdirp(prefix + '/man/man1')
        mkdirp(prefix.lib)
        mkdirp(prefix.include)

        bins = ['mdb_stat', 'mdb_copy', 'mdb_dump', 'mdb_load']
        for f in bins:
            install(f, prefix.bin)

        mans = ['mdb_stat.1', 'mdb_copy.1', 'mdb_dump.1', 'mdb_load.1']
        for f in mans:
            install(f, prefix + '/man/man1')

        libs = ['liblmdb.a', 'liblmdb.so']
        for f in libs:
            install(f, prefix.lib)

        includes = ['lmdb.h']
        for f in includes:
            install(f, prefix.include)

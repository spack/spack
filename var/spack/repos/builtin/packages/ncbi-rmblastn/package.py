# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class NcbiRmblastn(AutotoolsPackage):
    """RMBlast search engine for NCBI."""

    homepage = "https://www.ncbi.nlm.nih.gov/"
    url      = "ftp://ftp.ncbi.nlm.nih.gov/blast/executables/rmblast/LATEST/ncbi-rmblastn-2.2.28-src.tar.gz"

    version('2.2.28', 'fb5f4e2e02ffcb1b17af2e9f206c5c22')
    version('2.6.0', 'c8ce8055b10c4d774d995f88c7cc6225',
            url='ftp://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/2.6.0/ncbi-blast-2.6.0+-src.tar.gz')

    patch('isb-2.6.0+-changes-vers2.patch', when='@2.6.0', level=1)

    configure_directory = 'c++'
    build_directory = 'c++'

    def configure_args(self):
        if self.spec.version < Version('2.6.0'):
            options = []
        elif self.spec.version == Version('2.6.0'):
            options = [
                '--without-internal',
                '--with-mt',
                '--without-debug',
                '--without-krb5',
                '--without-check',
                '--without-bz2',
                '--without-lzo',
                '--with-strip',
                '--with-ncbi-public',
                '--without-ncbi-c',
                '--without-sss',
                '--without-sssdb',
                '--without-vdb',
                '--without-pcre',
                '--without-gcrypt',
                '--without-nettle',
                '--without-gnutls',
                '--without-openssl',
                '--without-sybase',
                '--without-ftds',
                '--without-mysql',
                '--without-opengl',
                '--without-mesa',
                '--without-glut',
                '--without-glew',
                '--without-wxwidgets',
                '--without-freetype',
                '--without-ftgl',
                '--without-fastcgi',
                '--without-bdb',
                '--without-sp',
                '--without-orbacus',
                '--without-sqlite3',
                '--without-icu',
                '--without-expat',
                '--without-sablot',
                '--without-libxml',
                '--without-libxslt',
                '--without-libexslt',
                '--without-xerces',
                '--without-xalan',
                '--without-zorba',
                '--without-oechem',
                '--without-sge',
                '--without-muparser',
                '--without-hdf5',
                '--without-gif',
                '--without-png',
                '--without-tiff',
                '--without-xpm',
                '--without-magic',
                '--without-curl',
                '--without-mimetic',
                '--without-gsoap',
                '--without-avro',
                '--without-cereal',
                '--without-sasl2',
                '--without-mongodb',
                '--without-gmock',
                '--without-lapack',
                '--without-lmdb',
                '--without-3psw',
                '--without-local-lbsm',
                '--without-ncbi-crypt',
                '--without-connext',
                '--without-dbapi',
                '--without-ctools',
                '--without-gui',
                '--without-gbench'
            ]
        return options

    def install(self, spec, prefix):
        # make install fails with this version, override
        if spec.version == Version('2.6.0'):
            with working_dir('c++'):
                mkdirp(prefix.bin)
                install_tree('ReleaseMT/bin', prefix.bin)
        else:
            super().install(self, spec, prefix)

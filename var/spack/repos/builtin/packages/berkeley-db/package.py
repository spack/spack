# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class BerkeleyDb(AutotoolsPackage):
    """Oracle Berkeley DB"""

    homepage = "https://www.oracle.com/database/technologies/related/berkeleydb.html"
    url      = "https://fossies.org/linux/misc/db-18.1.32.tar.gz"

    version('18.1.32', sha256='fa1fe7de9ba91ad472c25d026f931802597c29f28ae951960685cde487c8d654')
    version('6.2.32',  sha256='a9c5e2b004a5777aa03510cfe5cd766a4a3b777713406b02809c17c8e0e7a8fb')
    version('6.1.29',  sha256='b3c18180e4160d97dd197ba1d37c19f6ea2ec91d31bbfaf8972d99ba097af17d')
    version('6.0.35',  sha256='24421affa8ae436fe427ae4f5f2d1634da83d3d55a5ad6354a98eeedb825de55')
    version('5.3.28',  sha256='e0a992d740709892e81f9d93f06daf305cf73fb81b545afe72478043172c3628')

    configure_directory = 'dist'
    build_directory = 'build_unix'

    def configure_args(self):
        return [
            '--disable-static',
            '--enable-cxx',
            '--enable-stl',
            # SSL support requires OpenSSL, but OpenSSL depends on Perl, which
            # depends on Berkey DB, creating a circular dependency
            '--with-repmgr-ssl=no',
        ]

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


class Rocksdb(MakefilePackage):
    """RocksDB: A Persistent Key-Value Store for Flash and RAM Storage"""

    homepage = "https://github.com/facebook/rocksdb"
    url      = 'https://github.com/facebook/rocksdb/archive/v5.17.2.tar.gz'
    git      = 'https://github.com/facebook/rocksdb.git'

    version('develop', git=git, branch='master', submodules=True)
    version('6.3.6', sha256='9878beb4e9b74a5f0d9500772235a39066fd019ba7af9ae6afe483ca713e3c7c')
    version('6.2.4', sha256='7f34d1b55501f5273d11cd064bd34aef87c51ff114452968b86457f06cdb8ced')
    version('6.2.2', sha256='3e7365cb2a35982e95e5e5dd0b3352dc78573193dafca02788572318c38483fb')
    version('6.1.2', sha256='df93f3b66caa1cbe1c2862c99c33e18a5c5b24a64fb51dfe8ef805e3c9fd1cad')
    version('6.1.1', sha256='f98abad7feeb40a0a77de4b3b7a58e70c9cd7f2780c40d9bd268adb12f095ee3')
    version('6.0.2', sha256='89e0832f1fb00ac240a9438d4bbdae37dd3e52f7c15c3f646dc26887da16f342')
    version('6.0.1', sha256='9a9aca15bc3617729d976ceb98f6cbd64c6c25c4d92f374b4897aa2d2faa07cf')
    version('5.18.3',  sha256='7fb6738263d3f2b360d7468cf2ebe333f3109f3ba1ff80115abd145d75287254')
    version('5.17.2',  sha256='101f05858650a810c90e4872338222a1a3bf3b24de7b7d74466814e6a95c2d28')
    version('5.16.6',  sha256='f0739edce1707568bdfb36a77638fd5bae287ca21763ce3e56cf0bfae8fff033')
    version('5.15.10', sha256='26d5d4259fa352ae1604b5b4d275f947cacc006f4f7d2ef0b815056601b807c0')
    version('5.14.3',  sha256='c7019a645fc23df0adfe97ef08e793a36149bff2f57ef3b6174cbb0c8c9867b1')
    version('5.13.4',  sha256='a1e1df858124961d9211134c98925cd478fd1c1863d38685fd74f42c44b656c2')
    version('5.12.5',  sha256='97ee9a0162bca38c0d303f7d4f3965337155eb74efd6270224a1d13e267dd7c8')

    variant('bz2', default=False, description='Enable bz2 compression support')
    variant('lz4', default=True, description='Enable lz4 compression support')
    variant('snappy', default=False, description='Enable snappy compression support')
    variant('static', default=True, description='Build static library')
    variant('zlib', default=True, description='Enable zlib compression support')
    variant('zstd', default=False, description='Enable zstandard compression support')

    depends_on('bzip2', when='+bz2')
    depends_on('gflags')
    depends_on('lz4', when='+lz4')
    depends_on('snappy', when='+snappy')
    depends_on('zlib', when='+zlib')
    depends_on('zstd', when='+zstd')

    # backport of https://github.com/facebook/rocksdb/commit/61876614dce8c9155e28d40b5d95ec1bf1cbfa47
    patch('gcc_warnings.patch')

    def build(self, spec, prefix):
        cflags = []
        ldflags = []

        if '+zlib' in self.spec:
            cflags.append('-I' + self.spec['zlib'].prefix.include)
            ldflags.append(self.spec['zlib'].libs.ld_flags)
        if '+bz2' in self.spec:
            cflags.append('-I' + self.spec['bzip2'].prefix.include)
            ldflags.append(self.spec['bzip2'].libs.ld_flags)

        for pkg in ['lz4', 'snappy', 'zstd']:
            if '+' + pkg in self.spec:
                cflags.append(self.spec[pkg].headers.cpp_flags)
                ldflags.append(self.spec[pkg].libs.ld_flags)

        cflags.append(self.spec['gflags'].headers.cpp_flags)
        ldflags.append(self.spec['gflags'].libs.ld_flags)

        env['CFLAGS'] = ' '.join(cflags)
        env['PLATFORM_FLAGS'] = ' '.join(ldflags)
        env['INSTALL_PATH'] = self.spec.prefix

        build_type = 'install-static' if '+static' in spec else 'install-shared'
        make(build_type)

    def install(self, spec, prefix):
        pass

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
import os

class Rocksdb(MakefilePackage):
    """RocksDB: A Persistent Key-Value Store for Flash and RAM Storage"""

    homepage = "https://github.com/facebook/rocksdb"
    url      = "https://github.com/facebook/rocksdb.git"

    version('master', git=url, submodules=True)
    version('v5.17.2', git=url, submodules=True)
    version('v5.15.10', git=url, submodules=True, preferred=True)
    version('v5.8.8', git=url, submodules=True)

    variant('static', default=True, description='Build static library')
    variant('zlib', default=True, description='Enable zlib compression support')
    variant('bz2', default=False, description='Enable bz2 compression support')
    variant('lz4', default=True, description='Enable lz4 compression support')
    variant('snappy', default=False, description='Enable snappy compression support')
    variant('zstd', default=False, description='Enable zstandard compression support')
    depends_on('zlib', when='+zlib')
    depends_on('bzip2', when='+bzip2')
    depends_on('lz4', when='+lz4')
    depends_on('snappy', when='+snappy')
    depends_on('zstd', when='+zstd')
    depends_on('gflags')

    def setup_environment(self, spack_env, run_env):
        cflags = []
        ldflags = []

        if '+zlib' in self.spec:
            cflags.append('-I' + self.spec['zlib'].prefix.include)
            ldflags.append(self.spec['zlib'].libs.ld_flags)
        if '+bz2' in self.spec:
            cflags.append('-I' + self.spec['bz2'].prefix.include)
            ldflags.append(self.spec['bz2'].libs.ld_flags)
        for pkg in ['lz4', 'snappy', 'zstd']: 
            if '+' + pkg in self.spec:
                cflags.append(self.spec[pkg].headers.cpp_flags)
                ldflags.append(self.spec[pkg].libs.ld_flags)
        
        cflags.append(self.spec['gflags'].headers.cpp_flags)
        ldflags.append(self.spec['gflags'].libs.ld_flags)
            
        spack_env.append_flags('CFLAGS',' '.join(cflags))
        spack_env.append_flags('PLATFORM_FLAGS',' '.join(ldflags))
        spack_env.append_flags('INSTALL_PATH', self.spec.prefix)
    
    def build(self, spec, prefix):
        build_type = ''
        if '+static' in spec: 
            build_type = 'install-static'
        else:
            build_type = 'install-shared'
        make(build_type)


    def install(self, spec, prefix):
        pass

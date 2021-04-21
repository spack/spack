# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Fdb(CMakePackage):
    """FDB (Fields DataBase) is a domain-specific object store developed at
    ECMWF for storing, indexing and retrieving GRIB data."""

    homepage = 'https://github.com/ecmwf/fdb'
    url = 'https://github.com/ecmwf/fdb/archive/refs/tags/5.7.0.tar.gz'

    maintainers = ['skosukhin']

    version('5.7.0', sha256='bbcb6a9b7e27c26a3ecff3fd83aa6c8e1ab20dc00d50c4fe22ba1df89b8bf9d6')

    variant('tools', default=True, description='Build the command line tools')
    variant('remote', default=True,
            description='Enable support for distributed remote FDB')
    variant(
        'backends',
        values=any_combination_of(
            # FDB backend in indexed filesystem with table-of-contents with
            # additional support for Lustre filesystem stripping control:
            'lustre',
            # Backends that will be added later:
            # FDB backend in persistent memory (NVRAM):
            # 'pmem',  # (requires https://github.com/ecmwf/pmem)
            # FDB backend in CEPH object store (using Rados):
            # 'rados'  # (requires eckit with RADOS support)
        ), description='List of supported backends')

    depends_on('cmake@3.12:', type='build')
    depends_on('ecbuild@3.4:', type='build')

    depends_on('eckit@1.16:')
    depends_on('eckit+admin', when='+tools+remote')

    depends_on('eccodes@2.10:')
    depends_on('metkit@1.5:+grib')

    depends_on('lustre', when='backends=lustre')

    # Starting version 1.7.0, metkit installs GribHandle.h to another directory.
    # We expect the next version of fdb to account for that:
    patch('metkit_1.7.0.patch', when='@5.7.0^metkit@1.7.0:')

    def cmake_args(self):
        enable_build_tools = '+tools' in self.spec

        args = [
            self.define('ENABLE_FDB_BUILD_TOOLS', enable_build_tools),
            self.define('ENABLE_BUILD_TOOLS', enable_build_tools),
            self.define_from_variant('ENABLE_FDB_REMOTE', 'remote'),
            # We cannot disable the FDB backend in indexed filesystem with
            # table-of-contents because some default test programs and tools
            # cannot be built without it:
            self.define('ENABLE_TOCFDB', True),
            self.define('ENABLE_LUSTRE', 'backends=lustre' in self.spec),
            self.define('ENABLE_PMEMFDB', False),
            self.define('ENABLE_RADOSFDB', False),
            # The tests download additional data (~10MB):
            self.define('ENABLE_TESTS', self.run_tests),
            # We do not need any experimental features:
            self.define('ENABLE_EXPERIMENTAL', False),
            self.define('ENABLE_SANDBOX', False)
        ]
        return args

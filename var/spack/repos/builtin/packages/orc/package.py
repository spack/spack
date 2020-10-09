# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install orc
#
# You can edit this file again by typing:
#
#     spack edit orc
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class Orc(CMakePackage):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://www.example.com"
    url      = "https://github.com/apache/orc/archive/rel/release-1.6.5.tar.gz"

    # FIXME: Add a list of GitHub accounts to
    # notify when the package is updated.
    # maintainers = ['github_user1', 'github_user2']

    version('1.6.5',  sha256='df5885db8fa2e4435db8d486c6c7fc4e2c565d6197eee27729cf9cbdf36353c0')

    # FIXME: Add dependencies if required.
    # depends_on('foo')
    depends_on('maven')
    depends_on('openssl')
    depends_on('zlib@1.2.11')
    depends_on('pcre')
    depends_on('protobuf@3.5.1')
    depends_on('zstd@1.4.5')
    depends_on('googletest@1.8.0')
    depends_on('snappy@1.1.7')
    depends_on('lz4@1.7.5')

    patch('thirdparty.patch')

    def cmake_args(self):
        # FIXME: Add arguments other than
        # FIXME: CMAKE_INSTALL_PREFIX and CMAKE_BUILD_TYPE
        # FIXME: If not needed delete this function
        args = []
        args.append('-DCMAKE_CXX_FLAGS=-fPIC')
        args.append('-DCMAKE_C_FLAGS=-fPIC')
        args.append('-DINSTALL_VENDORED_LIBS:BOOL=OFF')
        args.append('-DBUILD_LIBHDFSPP:BOOL=OFF')

        for x in ('snappy', 'zlib', 'zstd', 'lz4', 'protobuf'):
            args.append('-D{0}_HOME={1}'.format(x.upper(), self.spec[x].prefix))

        return args

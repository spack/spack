# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
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
#     spack install nss
#
# You can edit this file again by typing:
#
#     spack edit nss
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *

# TODO: Use gyp/ninja build system to have a faster compilation.


class Nss(MakefilePackage):
    """Network Security Services (NSS) is a set of libraries designed to support
    cross-platform development of security-enabled client and server
    applications."""

    homepage = "https://developer.mozilla.org/en-US/docs/Mozilla/Projects/NSS"

    version(
        '3.46.1',
        url=
        "https://ftp.Mozilla.org/pub/security/nss/releases/NSS_3_46_1_RTM/src/nss-3.46.1.tar.gz",
        sha256=
        '3bf7e0ed7db98803f134c527c436cc68415ff17257d34bd75de14e9a09d13651')

    # Compile instructions from Linux From Scratch:
    # see http://www.linuxfromscratch.org/blfs/view/cvs/postlfs/nss.html

    patch('nss-3.46.1-standalone-1.patch')
    parallel = False

    depends_on('zlib')
    depends_on('nspr')
    depends_on('sqlite@3:')

    build_directory = "nss"

    @property
    def build_targets(self):
        args = [
            'USE_SYSTEM_ZLIB=1', 'NSS_ENABLE_WERROR=0', 'USE_64=1',
            'BUILD_OPT=1', 'NSS_USE_SYSTEM_SQLITE=1'
        ]
        args.append('NSPR_INCLUDE_DIR={}/nspr'.format(
            self.spec['nspr'].prefix.include))
        return args

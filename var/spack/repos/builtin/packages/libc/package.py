# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package_defs import *


class Libc(BundlePackage):
    """Dummy package to provide interfaces available in libc."""

    homepage = "https://en.wikipedia.org/wiki/C_standard_library"

    version('1.0')  # Dummy

    variant('iconv', default=False, description='Provides interfaces for Localization Functions')
    variant('rpc', default=False, description='Provides interfaces for RPC')

    provides('iconv', when='+iconv')
    provides('rpc', when='+rpc')

    @property
    def libs(self):
        return LibraryList([])

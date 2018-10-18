# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Liblockfile(AutotoolsPackage):
    """NFS-safe locking library"""

    homepage = "https://github.com/miquels/liblockfile"
    url      = "https://github.com/miquels/liblockfile/archive/v1.14.tar.gz"

    version('1.14', '24ce9dbb34d7f508a52a91f762746ce3')

    patch('install_as_nonroot.patch')

    def configure_args(self):
        args = ['--enable-shared']
        return args

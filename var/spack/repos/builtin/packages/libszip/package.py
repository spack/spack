# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libszip(AutotoolsPackage):
    """Szip is an implementation of the extended-Rice lossless
     compression algorithm.

    It provides lossless compression of scientific data, and is
    provided with HDF software products.
    """

    homepage = "https://support.hdfgroup.org/doc_resource/SZIP/"
    url      = "https://support.hdfgroup.org/ftp/lib-external/szip/2.1.1/src/szip-2.1.1.tar.gz"
    list_url = "https://support.hdfgroup.org/ftp/lib-external/szip"
    list_depth = 3

    provides('szip')

    version('2.1.1', '5addbf2a5b1bf928b92c47286e921f72')
    version('2.1',   '902f831bcefb69c6b635374424acbead')

    def configure_args(self):
        return [
            '--enable-production',
            '--enable-shared',
            '--enable-static',
            '--enable-encoding',
        ]

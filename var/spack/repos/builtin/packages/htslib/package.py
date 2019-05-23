# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Htslib(AutotoolsPackage):
    """C library for high-throughput sequencing data formats."""

    homepage = "https://github.com/samtools/htslib"

    version('1.9', '2ac92c9c3eef9986345ac69a05dd4d24')
    version('1.8', '54e9b3a04251fa59b1878f6b546b5c79')
    version('1.7', 'd3cc7e080a9a8c4161d8f62b56d3b98d')
    version('1.6', 'd6fd14e208aca7e08cbe9072233d0af9')
    version('1.5', sha256='a02b515ea51d86352b089c63d778fb5e8b9d784937cf157e587189cb97ad922d')
    version('1.4', '2a22ff382654c033c40e4ec3ea880050')
    version('1.3.1', '16d78f90b72f29971b042e8da8be6843')
    version('1.2', '64026d659c3b062cfb6ddc8a38e9779f')

    depends_on('zlib')
    depends_on('bzip2', when="@1.4:")
    depends_on('xz', when="@1.4:")

    depends_on('m4', when="@1.2")
    depends_on('autoconf', when="@1.2")
    depends_on('automake', when="@1.2")
    depends_on('libtool', when="@1.2")

    # v1.2 uses the automagically assembled tarball from .../archive/...
    # everything else uses the tarballs uploaded to the release
    def url_for_version(self, version):
        if version.string == '1.2':
            return 'https://github.com/samtools/htslib/archive/1.2.tar.gz'
        else:
            url = "https://github.com/samtools/htslib/releases/download/{0}/htslib-{0}.tar.bz2"
            return url.format(version.dotted)

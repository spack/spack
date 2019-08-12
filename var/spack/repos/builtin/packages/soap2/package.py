# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Soap2(Package):
    """Software for short oligonucleotide alignment."""

    homepage = "http://soap.genomics.org.cn/soapaligner.html"
    url      = "http://soap.genomics.org.cn/down/soap2.21release.tar.gz"

    version('2.21', '563b8b7235463b68413f9e841aa40779')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        mkdirp(prefix.share.man)
        install('soap', prefix.bin)
        install('2bwt-builder', prefix.bin)
        install('soap.1', prefix.share.man)
        install('soap.man', prefix.share.man)

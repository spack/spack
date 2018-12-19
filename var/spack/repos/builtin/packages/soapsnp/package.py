# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Soapsnp(MakefilePackage):
    """SOAPsnp uses a method based on Bayes' theorem (the reverse probability
       model) to call consensus genotype by carefully considering the data
       quality, alignment, and recurring experimental errors."""

    homepage = "http://soap.genomics.org.cn/soapsnp.html"
    url      = "http://soap.genomics.org.cn/down/SOAPsnp-v1.03.tar.gz"

    version('1.03', '8d69e196013657357ff840b611762ebc')

    depends_on('boost')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install('soapsnp', prefix.bin)

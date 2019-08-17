# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Pcma(MakefilePackage):
    """PCMA is a progressive multiple sequence alignment program that combines
       two different alignment strategies."""

    homepage = "http://prodata.swmed.edu/pcma/pcma.php"
    url      = "http://prodata.swmed.edu/download/pub/PCMA/pcma.tar.gz"

    version('2.0', 'e78449b2f6b0e90348a0a6747d266f9b')

    def edit(self, spec, prefix):
        makefile = FileFilter('makefile')
        makefile.filter('gcc', spack_cc)

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install('pcma', prefix.bin)

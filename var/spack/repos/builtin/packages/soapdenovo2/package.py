# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Soapdenovo2(MakefilePackage):
    """SOAPdenovo is a novel short-read assembly method that can build a de
    novo draft assembly for the human-sized genomes. The program is
    specially designed to assemble Illumina GA short reads. It creates
    new opportunities for building reference sequences and carrying out
    accurate analyses of unexplored genomes in a cost effective way."""

    homepage = "https://github.com/aquaskyline/SOAPdenovo2"
    url = "https://github.com/aquaskyline/SOAPdenovo2/archive/r240.tar.gz"

    version("242", sha256="a0043ceb41bc17a1c3fd2b8abe4f9029a60ad3edceb2b15af3c2cfabd36aa11b")
    version("240", sha256="cc9e9f216072c0bbcace5efdead947e1c3f41f09baec5508c7b90f933a090909")

    def flag_handler(self, name, flags):
        if self.spec.satisfies("%gcc@10:"):
            if name == "cflags" or name == "CFLAGS":
                flags.append("-fcommon")
            if name == "cxxflags" or name == "CXXFLAGS":
                flags.append("-fcommon")
        return (flags, None, None)

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install("SOAPdenovo-63mer", prefix.bin)
        install("SOAPdenovo-127mer", prefix.bin)

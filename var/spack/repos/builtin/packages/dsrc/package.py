# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Dsrc(MakefilePackage):
    """DNA Sequence Reads Compression is an application designed for
    compression of data files containing reads from DNA sequencing in
    FASTQ format."""

    homepage = "http://sun.aei.polsl.pl/dsrc"
    url      = "https://github.com/refresh-bio/DSRC/archive/v2.0.2.tar.gz"

    version('2.0.2', '0a75deb6db948f9179df0756c259b870')

    parallel = False

    def install(self, spec, prefix):
        install_tree('bin', prefix.bin)
        install_tree('lib', prefix.lib)
        install_tree('include', prefix.include)
        install_tree('examples', prefix.examples)

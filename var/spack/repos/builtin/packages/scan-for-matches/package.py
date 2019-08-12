# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class ScanForMatches(Package):
    """scan_for_matches is a utility written in C for locating patterns in DNA
       or protein FASTA files."""

    homepage = "http://blog.theseed.org/servers/2010/07/scan-for-matches.html"
    url      = "http://www.theseed.org/servers/downloads/scan_for_matches.tgz"

    version('2010-7-16', 'f64c9cfb385984ded2a7ad9ad2253d83')

    def install(self, spec, prefix):
        cc = Executable(self.compiler.cc)
        cc('-O', '-o', 'scan_for_matches', 'ggpunit.c', 'scan_for_matches.c')
        mkdirp(prefix.bin)
        install('scan_for_matches', prefix.bin)

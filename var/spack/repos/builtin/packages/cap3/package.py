# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Cap3(Package):
    """CAP3 is DNA Sequence Assembly Program"""

    homepage = "http://seq.cs.iastate.edu/"
    url      = "http://seq.cs.iastate.edu/CAP3/cap3.linux.x86_64.tar"

    version('2015-02-11', '5393d937978ecc5f18fcb741140e1f02',
            url='http://seq.cs.iastate.edu/CAP3/cap3.linux.x86_64.tar')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install('cap3', prefix.bin)
        install('formcon', prefix.bin)
        mkdirp(prefix.doc)
        install('doc', prefix.doc)
        install('aceform', prefix.doc)

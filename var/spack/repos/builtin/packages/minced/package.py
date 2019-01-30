# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Minced(Package):
    """MinCED is a program to find Clustered Regularly Interspaced Short
    Palindromic Repeats (CRISPRs) in full genomes or environmental datasets
    such as metagenomes, in which sequence size can be anywhere from 100 to
    800 bp."""

    homepage = "https://github.com/ctSkennerton/minced"
    url      = "https://github.com/ctSkennerton/minced/archive/0.2.0.tar.gz"

    version('0.2.0', '32544f5a523f10fece6a127699e11245')

    depends_on('java', type=('build', 'run'))

    def install(self, spec, prefix):
        make()
        install('minced', prefix)
        install('minced.jar', prefix)

# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class SomaticSniper(CMakePackage):
    """A tool to call somatic single nucleotide variants."""

    homepage = "http://gmt.genome.wustl.edu/packages/somatic-sniper"
    url      = "https://github.com/genome/somatic-sniper/archive/v1.0.5.0.tar.gz"

    version('1.0.5.0', '64bc2b001c9a8089f2a05900f8a0abfe')

    depends_on('ncurses')

    parallel = False

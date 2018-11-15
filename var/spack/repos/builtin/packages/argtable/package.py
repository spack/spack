# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Argtable(AutotoolsPackage):
    """Argtable is an ANSI C library for parsing GNU style command line
       options with a minimum of fuss.
    """

    homepage = "http://argtable.sourceforge.net/"
    url      = "https://sourceforge.net/projects/argtable/files/argtable/argtable-2.13/argtable2-13.tar.gz/download"

    version('2-13', '156773989d0d6406cea36526d3926668')

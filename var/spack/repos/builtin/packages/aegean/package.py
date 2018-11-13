# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Aegean(MakefilePackage):
    """The AEGeAn Toolkit is designed for the Analysis and Evaluation of
       Genome Annotations. The toolkit includes a variety of analysis programs
       as well as a C library whose API provides access to AEGeAn's core
       functions and data structures."""

    homepage = "http://brendelgroup.github.io/AEGeAn/"
    url      = "https://github.com/BrendelGroup/AEGeAn/archive/v0.15.2.tar.gz"

    version('0.15.2', 'd7d73f5f132ff52340975b636564e949')

    depends_on('genometools')

    def edit(self, spec, prefix):
        makefile = FileFilter('Makefile')
        makefile.filter('/usr/local', prefix)

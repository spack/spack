# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Bbmap(Package):
    """Short read aligner for DNA and RNA-seq data."""

    homepage = "http://sourceforge.net/projects/bbmap/"
    url      = "https://downloads.sourceforge.net/project/bbmap/BBMap_37.36.tar.gz"

    version('37.36', '1e1086e1fae490a7d03c5a065b1c262f')

    depends_on('java')

    def install(self, spec, prefix):
        install_tree('.', prefix.bin)

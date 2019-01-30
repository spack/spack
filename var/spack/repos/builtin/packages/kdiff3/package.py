# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Kdiff3(Package):
    """Compare and merge 2 or 3 files or directories."""
    homepage = "http://kdiff3.sourceforge.net/"
    url      = "https://downloads.sourceforge.net/project/kdiff3/kdiff3/0.9.98/kdiff3-0.9.98.tar.gz"

    version('0.9.98', 'b52f99f2cf2ea75ed5719315cbf77446')

    depends_on("qt@5.2.0:")

    def install(self, spec, prefix):
        # make is done inside
        configure('qt4')

        # there is no make install, bummer...
        mkdirp(self.prefix.bin)
        install(join_path(self.stage.source_path, 'releaseQt', 'kdiff3'),
                self.prefix.bin)

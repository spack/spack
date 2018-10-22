# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Mpe2(Package):
    """Message Passing Extensions (MPE): Parallel, shared X window graphics"""

    homepage = "http://www.mcs.anl.gov/research/projects/perfvis/software/MPE/"
    url      = "http://ftp.mcs.anl.gov/pub/mpi/mpe/mpe2-1.3.0.tar.gz"

    version('1.3.0', '67bf0c7b2e573df3ba0d2059a96c2f7b')

    patch('mpe2.patch')

    depends_on("mpi")

    provides("mpe")

    def install(self, spec, prefix):
        configure("--prefix=" + prefix,
                  "--x-includes=/usr/X11R6/include",
                  "--x-libraries=/usr/X11R6/lib",
                  "--enable-mpe_graphics=yes",
                  "--disable-f77",
                  "--enable-viewers=no",
                  "--enable-slog2=no",
                  "--with-mpicc=mpicc")

        make()
        make("install")

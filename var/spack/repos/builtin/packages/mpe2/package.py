# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Mpe2(AutotoolsPackage):
    """Message Passing Extensions (MPE): Parallel, shared X window graphics"""

    homepage = "http://www.mcs.anl.gov/research/projects/perfvis/software/MPE/"
    url      = "http://ftp.mcs.anl.gov/pub/mpi/mpe/mpe2-1.3.0.tar.gz"

    version('1.3.0', '67bf0c7b2e573df3ba0d2059a96c2f7b')

    patch('mpe2.patch')

    depends_on("mpi")
    depends_on("libx11")

    provides("mpe")

    def configure_args(self):
        args = []

        args.append('--enable-mpe_graphics=yes')
        args.append('--disable-f77')
        args.append('--enable-viewers=no')
        args.append('--enable-slog2=no')
        args.append('--with-mpicc=%s' % self.spec['mpi'].mpicc)

        return args

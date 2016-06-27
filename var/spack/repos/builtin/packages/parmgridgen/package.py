##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################

from spack import *


class Parmgridgen(Package):
    """MGRIDGEN is a serial library written entirely in ANSI C that implements
    (serial) algorithms for obtaining a sequence of successive coarse grids
    that are well-suited for geometric multigrid methods.
    ParMGridGen is the parallel version of MGridGen
    """

    homepage = "http://www-users.cs.umn.edu/~moulitsa/software.html"
    url = "http://www-users.cs.umn.edu/~moulitsa/download/ParMGridGen-1.0.tar.gz"

    version('1.0', '2872fa95b7fb91d6bd525490eed62038')

    depends_on('mpi')

    def install(self, spec, prefix):
        make_opts = [
            'make=make',
            'COPTIONS=-fPIC',
            'LDOPTIONS=-fPIC',
            'CC={0}'.format(self.compiler.cc),
            'PARCC={0}'.format(spec['mpi'].mpicc),
            'LD={0}'.format(self.compiler.cc),
            'PARLD={0}'.format(spec['mpi'].mpicc),
            'LIBDIR=-L../..',
            'PARLIBS=-L../../ -lparmgrid -lmgrid -lm',
            'LIBS=-L../../ -lmgrid -lm',
            'parallel'
        ]

        make(*make_opts, parallel=False)

        mkdirp(prefix.include, prefix.lib, prefix.bin)

        install("mgridgen.h", prefix.include)
        install("parmgridgen.h", prefix.include)

        install("MGridGen/IMlib/libIMlib.a",
                join_path(prefix.lib, 'libIMlib.a'))
        install("libmgrid.a", prefix.lib)
        install("libparmgrid.a", prefix.lib)

        install("mgridgen", prefix.bin)
        install("parmgridgen", prefix.bin)

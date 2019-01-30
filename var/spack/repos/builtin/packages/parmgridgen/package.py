# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


# Note: should probably be named 'mgridgen+mpi' (as per scotch, metis etc)
class Parmgridgen(Package):
    """MGRIDGEN is a serial library written entirely in ANSI C that implements
    (serial) algorithms for obtaining a sequence of successive coarse grids
    that are well-suited for geometric multigrid methods.
    ParMGridGen is the parallel version of MGridGen.
    """

    homepage = "http://www-users.cs.umn.edu/~moulitsa/software.html"
    url = "http://www-users.cs.umn.edu/~moulitsa/download/ParMGridGen-1.0.tar.gz"

    version('1.0', '2872fa95b7fb91d6bd525490eed62038')

    variant('mpi', default=True,
            description='Activate the compilation of parallel libraries')

    depends_on('mpi', when='+mpi')

    def install(self, spec, prefix):
        make_opts = [
            'make=make',
            'COPTIONS={0}'.format(self.compiler.pic_flag),
            'LDOPTIONS={0}'.format(self.compiler.pic_flag),
            'CC={0}'.format(self.compiler.cc),
            'LD={0}'.format(self.compiler.cc),
            'LIBDIR=-L../..',
            'LIBS=-L../.. -lmgrid -lm',
        ]

        if '+mpi' in spec:
            make_opts.extend([
                'PARCC={0}'.format(spec['mpi'].mpicc),
                'PARLD={0}'.format(spec['mpi'].mpicc),
                'PARLIBS=-L../.. -lparmgrid -lmgrid -lm',
                'parallel'
            ])
        else:
            make_opts.append('serial')

        make(*make_opts, parallel=False)

        mkdirp(prefix.include, prefix.lib, prefix.bin)

        install("mgridgen.h", prefix.include)
        install("libmgrid.a", prefix.lib)
        install("mgridgen",   prefix.bin)

        if '+mpi' in spec:
            install("parmgridgen.h", prefix.include)
            install("libparmgrid.a", prefix.lib)
            install("parmgridgen",   prefix.bin)

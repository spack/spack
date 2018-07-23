##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
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
import glob


class Cohmm(MakefilePackage):
    """An anticipated important use-case for next-generation supercomputing
        is multiscale modeling, in which continuum equations for large-scale
        material deformation are augmented with high-fidelity, fine-scale
        simulations that provide constitutive data on demand.
    """
    tags = ['proxy-app']

    homepage = "http://www.exmatex.org/cohmm.html"
    git      = "https://github.com/exmatex/CoHMM.git"

    version('develop', branch='sad')

    variant('openmp', default=True, description='Build with OpenMP Support')
    variant('gnuplot', default=False, description='Enable gnu plot Support')
    depends_on('gnuplot', when='+gnuplot')

    def edit(self, spec, prefix):
        if '+openmp' in spec:
            filter_file('DO_OPENMP = O.*', 'DO_OPENMP = ON', 'Makefile')
        if '+gnuplot' in spec:
            filter_file('DO_GNUPLOT = O.*', 'DO_GNUPLOT = ON', 'Makefile')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        mkdirp(prefix.input)
        mkdirp(prefix.doc)
        install('cohmm', prefix.bin)
        install('README.md', prefix.doc)
        install('LICENSE.md', prefix.doc)
        for files in glob.glob('input/*.*'):
            install(files, prefix.input)

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


class Delly2(MakefilePackage):
    """Delly2 is an integrated structural variant prediction method that can
       discover, genotype and visualize deletions, tandem duplications,
       inversions and translocations at single-nucleotide resolution in
       short-read massively parallel sequencing data.."""

    homepage = "https://github.com/dellytools/delly"
    git      = "https://github.com/dellytools/delly.git"

    version('2017-08-03', commit='e32a9cd55c7e3df5a6ae4a91f31a0deb354529fc')

    depends_on('htslib')
    depends_on('boost')
    depends_on('bcftools')

    def edit(self, spec, prefix):
        # Only want to build delly source, not submodules. Build fails
        # using provided submodules, succeeds with existing spack recipes.
        makefile = FileFilter('Makefile')
        makefile.filter('HTSLIBSOURCES =', '#HTSLIBSOURCES')
        makefile.filter('BOOSTSOURCES =', '#BOOSTSOURCES')
        makefile.filter('SEQTK_ROOT ?=', '#SEQTK_ROOT')
        makefile.filter('BOOST_ROOT ?=', '#BOOST_ROOT')
        makefile.filter('cd src', '# cd src')
        makefile.filter('.htslib ', '')
        makefile.filter('.bcftools ', '')
        makefile.filter('.boost ', '')
        makefile.filter('.htslib:', '# .htslib:')
        makefile.filter('.bcftools:', '# .bcftools:')
        makefile.filter('.boost:', '# .boost:')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        with working_dir('src'):
            install('delly', prefix.bin)
            install('dpe', prefix.bin)
            install('cov', prefix.bin)

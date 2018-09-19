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


class Bucky(MakefilePackage):
    """BUCKy is a free program to combine molecular data from multiple loci.
       BUCKy estimates the dominant history of sampled individuals, and how
       much of the genome supports each relationship, using Bayesian
       concordance analysis."""

    homepage = "http://www.stat.wisc.edu/~ane/bucky/index.html"
    url      = "http://dstats.net/download/http://www.stat.wisc.edu/~ane/bucky/v1.4/bucky-1.4.4.tgz"

    version('1.4.4', 'f0c910dd1d411d112637826519943a6d')

    # Compilation requires gcc
    conflicts('%cce')
    conflicts('%clang')
    conflicts('%intel')
    conflicts('%nag')
    conflicts('%pgi')
    conflicts('%xl')
    conflicts('%xl_r')

    build_directory = 'src'

    def install(self, spec, prefix):
        with working_dir('src'):
            mkdirp(prefix.bin)
            install('bucky', prefix.bin)
            install('mbsum', prefix.bin)
        install_tree('data', prefix.data)
        install_tree('doc', prefix.doc)
        install_tree('scripts', prefix.scripts)

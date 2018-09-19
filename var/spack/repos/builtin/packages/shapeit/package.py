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


class Shapeit(Package):
    """SHAPEIT is a fast and accurate method for estimation of haplotypes (aka
       phasing) from genotype or sequencing data."""

    homepage = "https://mathgen.stats.ox.ac.uk/genetics_software/shapeit/shapeit.html"
    url      = "https://mathgen.stats.ox.ac.uk/genetics_software/shapeit/shapeit.v2.r837.GLIBCv2.12.Linux.dynamic.tgz"

    version('2.837', '895873bb655a0a985cbfd870fdd1dd60')

    def url_for_version(self, version):
        url = 'https://mathgen.stats.ox.ac.uk/genetics_software/shapeit/shapeit.v{0}.r{1}.GLIBCv2.12.Linux.dynamic.tgz'
        return url.format(version[0], version[1])

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        with working_dir('bin'):
            install('shapeit', prefix.bin)

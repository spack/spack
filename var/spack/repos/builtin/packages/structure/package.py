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


class Structure(MakefilePackage):
    """Structure is a free software package for using multi-locus genotype
       data to investigate population structure."""

    homepage = "http://web.stanford.edu/group/pritchardlab/structure.html"
    url      = "http://web.stanford.edu/group/pritchardlab/structure_software/release_versions/v2.3.4/structure_kernel_source.tar.gz"

    version('2.3.4', '4e0591678cdbfe79347d272b5dceeda1')

    depends_on('jdk', type=('build', 'run'))

    def url_for_version(self, version):
        url = "http://web.stanford.edu/group/pritchardlab/structure_software/release_versions/v{0}/structure_kernel_source.tar.gz"
        return url.format(version)

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install('structure', prefix.bin)
        install('mainparams', prefix.bin)
        install('extraparams', prefix.bin)

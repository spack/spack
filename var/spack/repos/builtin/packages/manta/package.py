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


class Manta(CMakePackage):
    """Structural variant and indel caller for mapped sequencing data"""

    homepage = "https://github.com/Illumina/manta"
    url      = "https://github.com/Illumina/manta/releases/download/v1.3.2/manta-1.3.2.release_src.tar.bz2"

    depends_on('boost@1.58.0:', type='build')
    depends_on('cmake@2.8.12:', type='build')
    depends_on('python@2.7.0:2.7.999', type=('build', 'run'))

    version('1.4.0', '582d10f3bc56aecfa5c24931af3742b4')
    version('1.3.2', '83f43fe1a12605c1e9803d1020b24bd1')
    version('1.3.1', 'e315caff775878872ee300ed34e8adae')
    version('1.3.0', '1243e2bb58ca7c9d69bbfbe528f492ec')

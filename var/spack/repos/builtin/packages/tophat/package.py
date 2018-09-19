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


class Tophat(AutotoolsPackage):
    """Spliced read mapper for RNA-Seq."""

    homepage = "http://ccb.jhu.edu/software/tophat/index.shtml"
    url      = "https://github.com/infphilo/tophat/archive/v2.1.1.tar.gz"

    version('2.1.2', 'db844fd7f53c519e716cd6222e6195b2')
    version('2.1.1', 'ffd18de2f893a95eb7e9d0c5283d241f')

    depends_on('autoconf', type='build')
    # 2.1.1 only builds with automake@1.15.1.  There's a patch here:
    # https://github.com/spack/spack/pull/8244, which was incorporated
    # upstream in 2.1.2, which is known to build with 1.16.1 and 1.15.1.
    depends_on('automake',                        type='build')
    depends_on('automake@1.15.1', when='@:2.1.1', type='build')
    depends_on('libtool',  type='build')
    depends_on('m4',       type='build')

    depends_on('boost@1.47:')
    depends_on('bowtie2', type='run')

    parallel = False

    def configure_args(self):
        return ["--with-boost={0}".format(self.spec['boost'].prefix)]

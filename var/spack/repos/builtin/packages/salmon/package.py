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


class Salmon(CMakePackage):
    """Salmon is a tool for quantifying the expression of transcripts using
       RNA-seq data."""

    homepage = "http://combine-lab.github.io/salmon/"
    url      = "https://github.com/COMBINE-lab/salmon/archive/v0.8.2.tar.gz"

    version('0.9.1', '1277b8ed65d2c6982ed176a496a2a1e3')
    version('0.8.2', 'ee512697bc44b13661a16d4e14cf0a00')

    depends_on('tbb')
    depends_on('boost@:1.66.0')

    def cmake_args(self):
        args = ['-DBOOST_ROOT=%s' % self.spec['boost'].prefix]
        return args

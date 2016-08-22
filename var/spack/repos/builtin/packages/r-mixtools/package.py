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


class RMixtools(Package):
    """
    A collection of R functions for analyzing finite mixture models.
    """

    homepage = "http://www.example.co://cran.r-project.org/web/packages/mixtools/index.html"
    url      = "https://cran.r-project.org/src/contrib/mixtools_1.0.4.tar.gz"
    url_list = "https://cran.r-project.org/src/contrib/Archive/mixtools"

    version('1.0.4', 'c0e6ec44d16ec8914797fb74a651d3e5')

    extends('R')

    depends_on('r-segmented')
    depends_on('r-mass')
    depends_on('r-boot')
 
    def install(self, spec, prefix):
        # FIXME: Add logic to build and install here.
        R('CMD', 'INSTALL', '--library={0}'.format(self.module.r_lib_dir),
          self.stage.source_path)

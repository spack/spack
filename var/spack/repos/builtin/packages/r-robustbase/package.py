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


class RRobustbase(Package):
    """"
    Essential" Robust Statistics. Tools allowing to analyze data with robust
    methods. This includes regression methodology including model selections
    and multivariate statistics where we strive to cover the book "Robust
    Statistics, Theory and Methods" by 'Maronna, Martin and Yohai';
    Wiley 2006.
    """

    homepage = "http://www.example.co://cran.r-project.org/web/packages/robustbase/index.html"
    url      = "https://cran.r-project.org/src/contrib/robustbase_0.92-6.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/robustbase"

    version('0.92-6', '62e25dfbb6a29d1d6bc93840caede8d9')

    extends('R')

    depends_on('r-deoptimr')

    def install(self, spec, prefix):
        R('CMD', 'INSTALL', '--library={0}'.format(self.module.r_lib_dir),
          self.stage.source_path)

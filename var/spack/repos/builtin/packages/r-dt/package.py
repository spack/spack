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


class RDt(Package):
    """Data objects in R can be rendered as HTML tables using the JavaScript
    library 'DataTables' (typically via R Markdown or Shiny). The 'DataTables'
    library has been included in this R package. The package name 'DT' is an
    abbreviation of 'DataTables'."""

    homepage = "http://rstudio.github.io/DT"
    url      = "https://cran.r-project.org/src/contrib/DT_0.1.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/DT/"

    version('0.1', '5c8df984921fa484784ec4b8a4fb6f3c')

    extends('R')

    depends_on('r-htmltools', type=nolink)
    depends_on('r-htmlwidgets', type=nolink)
    depends_on('r-magrittr', type=nolink)

    def install(self, spec, prefix):
        R('CMD', 'INSTALL', '--library={0}'.format(self.module.r_lib_dir),
          self.stage.source_path)

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


class RDevtools(Package):
    """Collection of package development tools."""

    homepage = "https://github.com/hadley/devtools"
    url = "https://cran.r-project.org/src/contrib/devtools_1.11.1.tar.gz"

    version('1.11.1', '242672ee27d24dddcbdaac88c586b6c2')

    extends('R')

    depends_on('r-httr')
    depends_on('r-memoise')
    depends_on('r-whisker')
    depends_on('r-digest')
    depends_on('r-rstudioapi')
    depends_on('r-jsonlite')
    depends_on('r-git2r')
    depends_on('r-withr')

    def install(self, spec, prefix):
        R('CMD', 'INSTALL', '--library={0}'.format(self.module.r_lib_dir),
          self.stage.source_path)

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


class RR6(RPackage):
    """The R6 package allows the creation of classes with reference semantics,
    similar to R's built-in reference classes. Compared to reference classes,
    R6 classes are simpler and lighter-weight, and they are not built on S4
    classes so they do not require the methods package. These classes allow
    public and private members, and they support inheritance, even when the
    classes are defined in different packages."""

    homepage = "https://github.com/wch/R6/"
    url      = "https://cran.r-project.org/src/contrib/R6_2.2.0.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/R6"

    version('2.2.0', '659d83b2d3f7a308a48332b4cfbdab49')
    version('2.1.2', 'b6afb9430e48707be87638675390e457')

    depends_on('r@3.0:')

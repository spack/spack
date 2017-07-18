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


class RCommonmark(RPackage):
    """The CommonMark specification defines a rationalized version of markdown
    syntax. This package uses the 'cmark' reference implementation for
    converting markdown text into various formats including html, latex and
    groff man. In addition it exposes the markdown parse tree in xml format.
    The latest version of this package also adds support for Github extensions
    including tables, autolinks and strikethrough text."""

    homepage = "https://github.com/jeroenooms/commonmark"
    url      = "https://cran.r-project.org/src/contrib/commonmark_1.2.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/commonmark"

    version('1.2', 'b2dc0df43ab1ae0e3a4703cc90440f69')

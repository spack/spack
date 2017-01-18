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


class RXml(RPackage):
    """Many approaches for both reading and creating XML (and HTML) documents
    (including DTDs), both local and accessible via HTTP or FTP. Also offers
    access to an 'XPath' "interpreter"."""

    homepage = "http://www.omegahat.net/RSXML"
    url      = "https://cran.r-project.org/src/contrib/XML_3.98-1.4.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/XML"

    version('3.98-1.5', 'd1cfcd56f7aec96a84ffca91aea507ee')
    version('3.98-1.4', '1a7f3ce6f264eeb109bfa57bedb26c14')

    depends_on('libxml2')

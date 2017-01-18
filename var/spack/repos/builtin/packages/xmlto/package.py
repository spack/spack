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


class Xmlto(AutotoolsPackage):
    """Utility xmlto is a simple shell script for converting XML files to various
    formats. It serves as easy to use command line frontend to make fine output
    without remembering many long options and searching for the syntax of the
    backends."""

    homepage = "http://cyberelk.net/tim/software/xmlto/"
    url      = "https://fedorahosted.org/releases/x/m/xmlto/xmlto-0.0.28.tar.gz"

    version('0.0.28', 'a1fefad9d83499a15576768f60f847c6')

    # FIXME: missing a lot of dependencies
    depends_on('libxslt')

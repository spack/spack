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


class Mxml(AutotoolsPackage):
    """Mini-XML is a small XML library that you can use to read and write XML
    and XML-like data files in your application without requiring large
    non-standard libraries.
    """

    homepage = "http://www.msweet.org"
    url = "http://www.msweet.org/files/project3/mxml-2.9.tar.gz"

    version('2.9', 'e21cad0f7aacd18f942aa0568a8dee19')
    version('2.8', 'd85ee6d30de053581242c4a86e79a5d2')
    version('2.7', '76f2ae49bf0f5745d5cb5d9507774dc9')
    version('2.6', '68977789ae64985dddbd1a1a1652642e')
    version('2.5', 'f706377fba630b39fa02fd63642b17e5')

    # module swap PrgEnv-intel PrgEnv-$COMP
    # (Can use whatever compiler you want to use)
    # Case statement to change CC and CXX flags

    def configure_args(self):
        return ['--disable-shared', 'CFLAGS=-static']

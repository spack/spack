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


class Datamash(AutotoolsPackage):
    """GNU datamash is a command-line program which performs basic numeric,
    textual and statistical operations on input textual data files.
    """

    homepage = "https://www.gnu.org/software/datamash/"
    url      = "http://ftp.gnu.org/gnu/datamash/datamash-1.0.5.tar.gz"

    version('1.1.0', '79a6affca08107a095e97e4237fc8775')
    version('1.0.7', '9f317bab07454032ba9c068e7f17b04b')
    version('1.0.6', 'ff26fdef0f343cb695cf1853e14a1a5b')
    version('1.0.5', '9a29549dc7feca49fdc5fab696614e11')

##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
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


class PopplerData(CMakePackage):
    """This package consists of encoding files for use with poppler. The
    encoding files are optional and poppler will automatically read them if
    they are present.  When installed, the encoding files enables poppler to
    correctly render CJK and Cyrrilic properly.  While poppler is licensed
    under the GPL, these encoding files have different license, and thus
    distributed separately."""

    homepage = "https://poppler.freedesktop.org/"
    url      = "https://poppler.freedesktop.org/poppler-data-0.4.9.tar.gz"

    version('0.4.9', '35cc7beba00aa174631466f06732be40')

    depends_on('cmake@2.6:', type='build')

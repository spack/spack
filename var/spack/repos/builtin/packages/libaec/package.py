##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
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


class Libaec(CMakePackage):
    """Libaec provides fast lossless compression of 1 up to 32 bit wide signed
       or unsigned integers (samples). It implements Golomb-Rice compression
       method under the BSD license and includes a free drop-in replacement for
       the SZIP library.
    """

    homepage = 'https://gitlab.dkrz.de/k202009/libaec'
    url = 'https://gitlab.dkrz.de/k202009/libaec/uploads/631e85bcf877c2dcaca9b2e6d6526339/libaec-1.0.0.tar.gz'
    list_url = 'https://gitlab.dkrz.de/k202009/libaec/tags'

    provides('szip')

    version('1.0.1', 'cdf70e2b8f9153ee644710bb441f9e1e')
    version('1.0.0', 'a848b4e397ed210313183a5e92592e42')

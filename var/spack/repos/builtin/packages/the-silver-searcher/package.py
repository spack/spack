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


class TheSilverSearcher(AutotoolsPackage):
    """Fast recursive grep alternative"""

    homepage = "http://geoff.greer.fm/ag/"
    url      = "http://geoff.greer.fm/ag/releases/the_silver_searcher-0.32.0.tar.gz"

    version('2.1.0', '3e7207b060424174323236932bf76ec2')
    version('0.32.0', '3fdfd5836924246073d5344257a06823')
    version('0.30.0', '95e2e7859fab1156c835aff7413481db')

    depends_on('pcre')
    depends_on('xz')
    depends_on('zlib')
    depends_on('pkgconfig', type='build')

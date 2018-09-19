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


class Lzo(AutotoolsPackage):
    """Real-time data compression library"""

    homepage = 'https://www.oberhumer.com/opensource/lzo/'
    url = 'http://www.oberhumer.com/opensource/lzo/download/lzo-2.09.tar.gz'

    version('2.09', 'c7ffc9a103afe2d1bba0b015e7aa887f')
    version('2.08', 'fcec64c26a0f4f4901468f360029678f')
    version('2.07', '4011935e95171e78ad4894f7335c982a')
    version('2.06', '95380bd4081f85ef08c5209f4107e9f8')
    version('2.05', 'c67cda5fa191bab761c7cb06fe091e36')

    def configure_args(self):
        return [
            '--disable-dependency-tracking',
            '--enable-shared'
        ]

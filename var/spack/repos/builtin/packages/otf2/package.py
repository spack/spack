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


class Otf2(AutotoolsPackage):
    """The Open Trace Format 2 is a highly scalable, memory efficient event
       trace data format plus support library.
    """

    homepage = "http://www.vi-hps.org/projects/score-p"
    url      = "http://www.vi-hps.org/upload/packages/otf2/otf2-1.4.tar.gz"

    version('2.1.1', 'e51ad0d8ca374d25f47426746ca629e7')
    version('2.1',   'e2994e53d9b7c2cbd0c4f564d638751e')
    version('2.0',   '5b546188b25bc1c4e285e06dddf75dfc')
    version('1.5.1', '16a9df46e0da78e374f5d12c8cdc1109')
    version('1.4',   'a23c42e936eb9209c4e08b61c3cf5092')
    version('1.3.1', 'd0ffc4e858455ace4f596f910e68c9f2')
    version('1.2.1', '8fb3e11fb7489896596ae2c7c83d7fc8')

    def configure_args(self):
        return [
            '--enable-shared',
            'CFLAGS={0}'.format(self.compiler.pic_flag),
            'CXXFLAGS={0}'.format(self.compiler.pic_flag)
        ]

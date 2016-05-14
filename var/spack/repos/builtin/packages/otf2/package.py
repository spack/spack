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


class Otf2(Package):
    """
    The Open Trace Format 2 is a highly scalable, memory efficient event trace data format plus support library.
    """

    homepage = "http://www.vi-hps.org/score-p"
    url      = "http://www.vi-hps.org/upload/packages/otf2/otf2-1.4.tar.gz"

    version('2.0', '5b546188b25bc1c4e285e06dddf75dfc',
            url="http://www.vi-hps.org/upload/packages/otf2/otf2-2.0.tar.gz")
    version('1.5.1', '16a9df46e0da78e374f5d12c8cdc1109',
            url='http://www.vi-hps.org/upload/packages/otf2/otf2-1.5.1.tar.gz')
    version('1.4',   'a23c42e936eb9209c4e08b61c3cf5092',
            url="http://www.vi-hps.org/upload/packages/otf2/otf2-1.4.tar.gz")
    version('1.3.1', 'd0ffc4e858455ace4f596f910e68c9f2',
            url="http://www.vi-hps.org/upload/packages/otf2/otf2-1.3.1.tar.gz")
    version('1.2.1', '8fb3e11fb7489896596ae2c7c83d7fc8',
            url="http://www.vi-hps.org/upload/packages/otf2/otf2-1.2.1.tar.gz")

    def install(self, spec, prefix):
        configure_args=["--prefix=%s" % prefix,
                        "--enable-shared",
                        "CFLAGS=-fPIC",
                        "CXXFLAGS=-fPIC"]
        configure(*configure_args)
        make()
        make("install")

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


class Curl(Package):
    """cURL is an open source command line tool and library for
    transferring data with URL syntax"""

    homepage = "http://curl.haxx.se"
    url      = "http://curl.haxx.se/download/curl-7.46.0.tar.bz2"

    version('7.52.1', 'dd014df06ff1d12e173de86873f9f77a')
    version('7.50.3', 'bd177fd6deecce00cfa7b5916d831c5e')
    version('7.50.2', '6e161179f7af4b9f8b6ea21420132719')
    version('7.50.1', '015f6a0217ca6f2c5442ca406476920b')
    version('7.49.1', '6bb1f7af5b58b30e4e6414b8c1abccab')
    version('7.47.1', '9ea3123449439bbd960cd25cf98796fb')
    version('7.46.0', '9979f989a2a9930d10f1b3deeabc2148')
    version('7.45.0', '62c1a352b28558f25ba6209214beadc8')
    version('7.44.0', '6b952ca00e5473b16a11f05f06aa8dae')
    version('7.43.0', '11bddbb452a8b766b932f859aaeeed39')
    version('7.42.1', '296945012ce647b94083ed427c1877a8')

    depends_on("openssl")
    depends_on("zlib")

    def install(self, spec, prefix):
        configure('--prefix=%s' % prefix,
                  '--with-zlib=%s' % spec['zlib'].prefix,
                  '--with-ssl=%s' % spec['openssl'].prefix)

        make()
        make("install")

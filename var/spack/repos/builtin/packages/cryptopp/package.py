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
import glob
from spack import *


class Cryptopp(Package):
    """Crypto++ is an open-source C++ library of cryptographic schemes. The
       library supports a number of different cryptography algorithms,
       including authenticated encryption schemes (GCM, CCM), hash
       functions (SHA-1, SHA2), public-key encryption (RSA, DSA), and a
       few obsolete/historical encryption algorithms (MD5, Panama).

    """

    homepage = "http://www.cryptopp.com"

    version('5.6.3', '3c5b70e2ec98b7a24988734446242d07')
    version('5.6.2', '7ed022585698df48e65ce9218f6c6a67')
    version('5.6.1', '96cbeba0907562b077e26bcffb483828')

    def url_for_version(self, version):
        url = "{0}/{1}{2}.zip"
        return url.format(self.homepage, self.name, version.joined)

    def install(self, spec, prefix):
        make()

        mkdirp(prefix.include)
        for hfile in glob.glob('*.h*'):
            install(hfile, prefix.include)

        mkdirp(prefix.lib)
        install('libcryptopp.a', prefix.lib)

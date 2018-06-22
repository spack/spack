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


class Minuit(AutotoolsPackage):
    """MINUIT is a physics analysis tool for function minimization."""

    homepage = "https://seal.web.cern.ch/seal/snapshot/work-packages/mathlibs/minuit/home.html"
    url      = "http://www.cern.ch/mathlibs/sw/5_34_14/Minuit2/Minuit2-5.34.14.tar.gz"
    list_url = "https://seal.web.cern.ch/seal/snapshot/work-packages/mathlibs/minuit/release/download.html"

    version('5.34.14', '7fc00378a2ed1f731b719d4837d62d6a')
    version('5.28.00', '536a1d29e5cc9bd4499d17d665021370')
    version('5.27.02', 'b54673f2b9b62a8ff4e6937a2ed8fda5')
    version('5.24.00', '9a915e56bee1e8986a719aa80e7b05d6')
    version('5.22.00', '2cbc34907bfe202c7a779e9713355846')
    version('5.21.06', 'b431ed129abb6c5020fd58d53cb8d27c')
    version('5.20.00', '3083d31e3764de45d477d082d60f2c29')
    version('5.18.00', 'a8764e7213fe811e56d5b6e5f3a91f5e')
    version('5.16.00', '6ea5feca06fca365d324bcfe16db7f08')
    version('5.14.00', 'b7452867b01c76cd115c696336c202d2')
    version('5.12.00', '36726b8c6fcddf4f0837c900461a1d3c')
    version('5.10.00', 'dfc7afc0add70deaca105ff549f5a786')
    version('5.08.00', '1cc8da07c4a247c877f39acf8d76ba02')
    version('1.7.9', '10fd518fc778317fdadbc4ef6f7ce8e4')
    version('1.7.6', '6a9a8341557de154274caff810686364')
    version('1.7.1', 'd202a1cf58662e9833f2967b4dc8808e')
    version('1.6.3', '955f560d0fb17bd7f081eddd7080fad6')
    version('1.6.0', '6992d70fc8fded50be49b6b358b58507')
    version('1.5.2', '31a0698febe59edd70aa001c4d7a56f8')
    version('1.5.0', 'bc502c66af071fcdc0a2ae45a8740c75')

    def url_for_version(self, version):
        if version > Version('5.0.0'):
            url = "http://www.cern.ch/mathlibs/sw/{0}/Minuit2/Minuit2-{1}.tar.gz"
            return url.format(version.underscored, version)
        else:
            url = "http://seal.web.cern.ch/seal/minuit/releases/Minuit-{0}.tar.gz"
            return url.format(version.underscored)

    patch('sprintf.cxx.patch', when='@5.08.00:5.18.00')
    patch('sprintf.patch', when='@:1.7.9')
    patch('LASymMatrix.h.patch', when='@:1.7.6')

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


class Openssh(AutotoolsPackage):
    """OpenSSH is the premier connectivity tool for remote login with the
       SSH protocol. It encrypts all traffic to eliminate
       eavesdropping, connection hijacking, and other attacks. In
       addition, OpenSSH provides a large suite of secure tunneling
       capabilities, several authentication methods, and sophisticated
       configuration options.
    """

    homepage = "https://www.openssh.com/"
    url      = "https://mirrors.sonic.net/pub/OpenBSD/OpenSSH/portable/openssh-7.6p1.tar.gz"

    version('7.6p1',   '06a88699018e5fef13d4655abfed1f63')
    version('7.5p1',   '652fdc7d8392f112bef11cacf7e69e23')
    version('7.4p1',   'b2db2a83caf66a208bb78d6d287cdaa3')
    version('7.3p1',   'dfadd9f035d38ce5d58a3bf130b86d08')
    version('7.2p2',   '13009a9156510d8f27e752659075cced')
    version('7.1p2',   '4d8547670e2a220d5ef805ad9e47acf2')
    version('7.0p1',   '831883f251ac34f0ab9c812acc24ee69')
    version('6.9p1',   '0b161c44fc31fbc6b76a6f8ae639f16f')
    version('6.8p1',   '08f72de6751acfbd0892b5f003922701')
    version('6.7p1',   '3246aa79317b1d23cae783a3bf8275d6')
    version('6.6p1',   '3e9800e6bca1fbac0eea4d41baa7f239')

    depends_on('openssl')
    depends_on('libedit')
    depends_on('ncurses')
    depends_on('zlib')

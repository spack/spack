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


class Node(AutotoolsPackage):
    """
    Node.js is a JavaScript runtime built on Chrome's V8 JavaScript engine.
    """

    homepage = "https://nodejs.org"
    url      = "https://nodejs.org/dist/v8.11.3/node-v8.11.3.tar.gz"

    version('10.7.0', sha256='b9691cbc6e6a2e209a9b8cb88fd942802236dae06652080f582304dbdd505ad2')
    version('9.11.2', sha256='4a9cf0bfdf6a0e8c454d21517f70fc2c05a99d7055571826939096172a7040f6')
    version('8.11.3', sha256='0d7e795c0579226c8b197353bbb9392cae802f4fefa4787a2c0e678beaf85cce')
    version('7.10.1', sha256='baf060e5d3abb8fdebb8c2b28c4d8cde05d43acfd9fc687f21f4b7a3ff69745e')
    version('6.14.3', sha256='378b7b06ce6de96c59970908fc2a67278e1ece22be78030423297bf415c0a8c5')
    version('5.12.0', sha256='250c12a561d7319e71e142ee92ab682494c7823d81ce24703c80eb52bdf9ba42')
    version('4.9.1',  sha256='d2bc20dbe2c20e6f606671b1b9631f0d20396547ac7cbc144a3dad2c78106c78')

    depends_on('python@2.6:', type='build')

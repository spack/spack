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


class Sbt(Package):
    """Scala Build Tool"""

    homepage = 'http://www.scala-sbt.org'
    url      = "https://github.com/sbt/sbt/releases/download/v1.1.4/sbt-1.1.4.tgz"

    version('1.1.6', 'd307b131ed041c783ac5ed7bbb4768dc')
    version('1.1.5', 'b771480feb07f98fa8cd6d787c8d4485')
    version('1.1.4', 'c71e5fa846164d14d4cd450520d66c6a')
    version('0.13.17', 'c52c6152cc7aadfd1f0736a1a5d0a5b8')

    depends_on('java')

    def install(self, spec, prefix):
        install_tree('bin',  prefix.bin)
        install_tree('conf', prefix.conf)

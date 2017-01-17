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
import shutil


class Sbt(Package):
    """Scala Build Tool"""

    homepage = "http://www.scala-sbt.org"
    url      = "https://dl.bintray.com/sbt/native-packages/sbt/0.13.12/sbt-0.13.12.tgz"

    version('0.13.12', 'cec3071d46ef13334c8097cc3467ff28')

    depends_on('jdk')

    def install(self, spec, prefix):
        shutil.copytree('bin', join_path(prefix, 'bin'), symlinks=True)
        shutil.copytree('conf', join_path(prefix, 'conf'), symlinks=True)

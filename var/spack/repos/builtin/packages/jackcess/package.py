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


class Jackcess(Package):
    """Jackcess is a pure Java library for reading from and writing to
    MS Access databases (currently supporting versions 2000-2016)."""

    homepage = "http://jackcess.sourceforge.net/"
    url      = "https://sourceforge.net/projects/jackcess/files/jackcess/2.1.12/jackcess-2.1.12.jar"

    version('2.1.12',   '7d051d8dd93f2fe7e5e86389ea380619', expand=False)
    version('1.2.14.3', 'ef778421c1385ac9ab4aa7edfb954caa', expand=False)

    extends('jdk')
    depends_on('java', type='run')
    depends_on('commons-lang@2.6', when='@2.1.12', type='run')
    depends_on('commons-lang@2.4', when='@1.2.14.3', type='run')
    depends_on('commons-logging@1.1.3', when='@2.1.12', type='run')
    depends_on('commons-logging@1.1.1', when='@1.2.14.3', type='run')

    def install(self, spec, prefix):
        install('jackcess-{0}.jar'.format(self.version), prefix)

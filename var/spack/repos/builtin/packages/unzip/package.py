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


class Unzip(MakefilePackage):
    """Unzip is a compression and file packaging/archive utility."""

    homepage = 'http://www.info-zip.org/Zip.html'
    url      = 'http://downloads.sourceforge.net/infozip/unzip60.tar.gz'

    version('6.0', '62b490407489521db863b523a7f86375')

    conflicts('platform=cray', msg='Unzip does not currently build on Cray')

    make_args = ['-f', 'unix/Makefile']
    build_targets = make_args + ['generic']

    def url_for_version(self, version):
        return 'http://downloads.sourceforge.net/infozip/unzip{0}.tar.gz'.format(version.joined)

    @property
    def install_targets(self):
        return self.make_args + ['prefix={0}'.format(self.prefix), 'install']

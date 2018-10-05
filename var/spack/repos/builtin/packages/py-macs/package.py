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


class PyMacs(PythonPackage):
    """MACS Model-based Analysis of ChIP-Seq.

    There are currently two versions widely used: 1.4.2-1 and 2.1.1.20160309.

    Homepage for v1: http://liulab.dfci.harvard.edu/MACS/index.html.
    Homepage for v2: https://github.com/taoliu/MACS.
    """

    homepage = "https://github.com/taoliu/MACS"
    url      = "https://pypi.io/packages/source/M/MACS2/MACS2-2.1.1.20160309.tar.gz"

    version('2.1.1.20160309',
            '2008ba838f83f34f8e0fddefe2a3a0159f4a740707c68058f815b31ddad53d26',
            url='https://pypi.io/packages/source/M/MACS2/MACS2-2.1.1.20160309.tar.gz')
    version('1.4.2-1',
            '950dab09fe1335c8bbb34a896c21e3e2',
            url="https://github.com/downloads/taoliu/MACS/MACS-1.4.2-1.tar.gz")

    depends_on('python@2.6:2.7', when='@:1.999')
    depends_on('python@2.7:2.8', when='@2:')

    depends_on('py-setuptools', type=('build', 'run'), when='@2:')
    depends_on('py-numpy@1.6:', type=('build', 'run'), when='@2:')

    def url_for_version(self, version):
        if version < Version('2'):
            url = "https://github.com/downloads/taoliu/MACS/MACS-{0}.tar.gz".format(version)
        else:
            url = "https://pypi.io/packages/source/M/MACS{0}/MACS{1}-{2}.tar.gz".format(version.up_to(1), version.up_to(1), version)
        return url

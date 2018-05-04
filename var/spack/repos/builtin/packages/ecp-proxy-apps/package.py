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

import os
from spack import *


class EcpProxyApps(Package):
    """This is a collection of packages that represents the official suite of
       DOE/ECP proxy applications. This is a Spack bundle package that
       installs the ECP proxy application suite.
    """

    homepage = "https://exascaleproject.github.io/proxy-apps"

    # Dummy url
    url = 'https://github.com/exascaleproject/proxy-apps/archive/v1.0.tar.gz'

    tags = ['proxy-app', 'ecp-proxy-app']

    version('1.0', '5a26b184f506afeb7d221f15c0e8f153')

    depends_on('amg@1.0', when='@1.0')
    depends_on('candle-benchmarks@1.0', when='@1.0')
    depends_on('comd@1.1', when='@1.0')
    depends_on('laghos@1.0', when='@1.0')
    depends_on('macsio@1.0', when='@1.0')
    depends_on('miniamr@1.4.0', when='@1.0')
    depends_on('minife@2.1.0', when='@1.0')
    depends_on('minitri@1.0', when='@1.0')
    depends_on('nekbone@17.0', when='@1.0')
    depends_on('sw4lite@1.0', when='@1.0')
    depends_on('swfft@1.0', when='@1.0')
    depends_on('xsbench@14', when='@1.0')

    # Dummy install for now,  will be removed when metapackage is available
    def install(self, spec, prefix):
        with open(os.path.join(spec.prefix, 'package-list.txt'), 'w') as out:
            for dep in spec.dependencies(deptype='build'):
                out.write("%s\n" % dep.format(
                    format_string='${PACKAGE} ${VERSION}'))
                os.symlink(dep.prefix, os.path.join(spec.prefix, dep.name))
            out.close()

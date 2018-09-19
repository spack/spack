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


class Httpie(PythonPackage):
    """Modern command line HTTP client."""

    homepage = "https://httpie.org/"
    url      = "https://pypi.io/packages/source/h/httpie/httpie-0.9.8.tar.gz"

    version('0.9.9', '13ed0b79b65e793eb288e563db38b2a2')
    version('0.9.8', 'e0d1af07d0959a2e081e7954797ce260')

    variant('socks', default=True,
            description='Enable SOCKS proxy support')

    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('py-pygments@2.1.3:', type=('build', 'run'))
    depends_on('py-requests@2.11.0:', type=('build', 'run'))
    depends_on('py-pysocks', type=('build', 'run'), when="+socks")
    # Concretization problem breaks this.  Unconditional for now...
    # https://github.com/spack/spack/issues/3628
    # depends_on('py-argparse@1.2.1:', type=('build', 'run'),
    #            when='^python@:2.6,3.0:3.1')
    depends_on('py-argparse@1.2.1:', type=('build', 'run'))
